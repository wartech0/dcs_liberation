import textwrap
from datetime import datetime
from typing import List, Optional, Callable

from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QMessageBox,
    QPushButton,
)

import qt_ui.uiconstants as CONST
from game import Game, persistence
from game.ato.package import Package
from game.ato.traveltime import TotEstimator
from game.profiling import logged_duration
from game.utils import meters
from qt_ui.models import GameModel
from qt_ui.simcontroller import SimController
from qt_ui.uiflags import UiFlags
from qt_ui.widgets.QBudgetBox import QBudgetBox
from qt_ui.widgets.QConditionsWidget import QConditionsWidget
from qt_ui.widgets.QFactionsInfos import QFactionsInfos
from qt_ui.widgets.QIntelBox import QIntelBox
from qt_ui.widgets.clientslots import MaxPlayerCount
from qt_ui.widgets.simspeedcontrols import SimSpeedControls
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal
from qt_ui.windows.QWaitingForMissionResultWindow import QWaitingForMissionResultWindow


class QTopPanel(QFrame):
    def __init__(
        self,
        game_model: GameModel,
        sim_controller: SimController,
        ui_flags: UiFlags,
        reset_to_pre_sim_checkpoint: Callable[[], None],
    ) -> None:
        super(QTopPanel, self).__init__()
        self.game_model = game_model
        self.sim_controller = sim_controller
        self.reset_to_pre_sim_checkpoint = reset_to_pre_sim_checkpoint
        self.dialog: Optional[QDialog] = None

        self.setMaximumHeight(70)

        self.conditionsWidget = QConditionsWidget(sim_controller)
        self.budgetBox = QBudgetBox(self.game)

        pass_turn_text = "Pass Turn"
        if not self.game or self.game.turn == 0:
            pass_turn_text = "Begin Campaign"
        self.passTurnButton = QPushButton(pass_turn_text)
        self.passTurnButton.setIcon(CONST.ICONS["PassTurn"])
        self.passTurnButton.setProperty("style", "btn-primary")
        self.passTurnButton.clicked.connect(self.passTurn)
        if not self.game:
            self.passTurnButton.setEnabled(False)

        self.proceedButton = QPushButton("Take off")
        self.proceedButton.setIcon(CONST.ICONS["Proceed"])
        self.proceedButton.setProperty("style", "start-button")
        self.proceedButton.clicked.connect(self.launch_mission)
        if not self.game or self.game.turn == 0:
            self.proceedButton.setEnabled(False)

        self.factionsInfos = QFactionsInfos(self.game)

        self.intel_box = QIntelBox(self.game)

        self.proceedBox = QGroupBox("Proceed")
        self.proceedBoxLayout = QHBoxLayout()
        if ui_flags.show_sim_speed_controls:
            self.proceedBoxLayout.addLayout(SimSpeedControls(sim_controller))
        self.proceedBoxLayout.addLayout(MaxPlayerCount(self.game_model.ato_model))
        self.proceedBoxLayout.addWidget(self.passTurnButton)
        self.proceedBoxLayout.addWidget(self.proceedButton)
        self.proceedBox.setLayout(self.proceedBoxLayout)

        self.layout = QHBoxLayout()

        self.layout.addWidget(self.factionsInfos)
        self.layout.addWidget(self.conditionsWidget)
        self.layout.addWidget(self.budgetBox)
        self.layout.addWidget(self.intel_box)
        self.layout.addStretch(1)
        self.layout.addWidget(self.proceedBox)

        self.layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.layout)

        GameUpdateSignal.get_instance().gameupdated.connect(self.setGame)
        GameUpdateSignal.get_instance().budgetupdated.connect(self.budget_update)

    @property
    def game(self) -> Optional[Game]:
        return self.game_model.game

    def setGame(self, game: Optional[Game]):
        if game is None:
            return

        self.conditionsWidget.setCurrentTurn(game.turn, game.conditions)

        if game.conditions.weather.clouds:
            base_m = game.conditions.weather.clouds.base
            base_ft = int(meters(base_m).feet)
            self.conditionsWidget.setToolTip(f"Cloud Base: {base_m}m / {base_ft}ft")
        else:
            self.conditionsWidget.setToolTip("")

        self.intel_box.set_game(game)
        self.budgetBox.setGame(game)
        self.factionsInfos.setGame(game)

        self.passTurnButton.setEnabled(True)
        if game and game.turn > 0:
            self.passTurnButton.setText("Pass Turn")

        if game and game.turn == 0:
            self.passTurnButton.setText("Begin Campaign")
            self.proceedButton.setEnabled(False)
        else:
            self.proceedButton.setEnabled(True)

    def passTurn(self):
        with logged_duration("Skipping turn"):
            self.game.pass_turn(no_action=True)
            GameUpdateSignal.get_instance().updateGame(self.game)
            self.proceedButton.setEnabled(True)

    def negative_start_packages(self, now: datetime) -> List[Package]:
        packages = []
        for package in self.game_model.ato_model.ato.packages:
            if not package.flights:
                continue
            for flight in package.flights:
                startup = flight.flight_plan.startup_time()
                if startup < now:
                    packages.append(package)
                    break
        return packages

    @staticmethod
    def fix_tots(packages: List[Package], now: datetime) -> None:
        for package in packages:
            estimator = TotEstimator(package)
            package.time_over_target = estimator.earliest_tot(now)

    def ato_has_clients(self) -> bool:
        for package in self.game.blue.ato.packages:
            for flight in package.flights:
                if flight.client_count > 0:
                    return True
        return False

    def confirm_no_client_launch(self) -> bool:
        result = QMessageBox.question(
            self,
            "Continue without player pilots?",
            (
                "No player pilots have been assigned to flights. Continuing will allow "
                "the AI to perform the mission, but players will be unable to "
                "participate.<br />"
                "<br />"
                "To assign player pilots to a flight, select a package from the "
                "Packages panel on the left of the main window, and then a flight from "
                "the Flights panel below the Packages panel. The edit button below the "
                "Flights panel will allow you to assign specific pilots to the flight. "
                "If you have no player pilots available, the checkbox next to the "
                "name will convert them to a player.<br />"
                "<br />Click 'Yes' to continue with an AI only mission"
                "<br />Click 'No' if you'd like to make more changes."
            ),
            QMessageBox.No,
            QMessageBox.Yes,
        )
        return result == QMessageBox.Yes

    def confirm_negative_start_time(self, negative_starts: List[Package]) -> bool:
        formatted = "<br />".join(
            [f"{p.primary_task} {p.target.name}" for p in negative_starts]
        )
        mbox = QMessageBox(
            QMessageBox.Question,
            "Continue with past start times?",
            (
                "Some flights in the following packages have start times set "
                "earlier than mission start time:<br />"
                "<br />"
                f"{formatted}<br />"
                "<br />"
                "Flight start times are estimated based on the package TOT, so it "
                "is possible that not all flights will be able to reach the "
                "target area at their assigned times.<br />"
                "<br />"
                "You can either continue with the mission as planned, with the "
                "misplanned flights potentially flying too fast and/or missing "
                "their rendezvous; automatically fix negative TOTs; or cancel "
                "mission start and fix the packages manually."
            ),
            parent=self,
        )
        auto = mbox.addButton("Fix TOTs automatically", QMessageBox.ActionRole)
        ignore = mbox.addButton("Continue without fixing", QMessageBox.DestructiveRole)
        cancel = mbox.addButton(QMessageBox.Cancel)
        mbox.setEscapeButton(cancel)
        mbox.exec_()
        clicked = mbox.clickedButton()
        if clicked == auto:
            self.fix_tots(negative_starts, self.sim_controller.current_time_in_sim)
            return True
        elif clicked == ignore:
            return True
        return False

    def check_no_missing_pilots(self) -> bool:
        missing_pilots = []
        for package in self.game.blue.ato.packages:
            for flight in package.flights:
                if flight.missing_pilots > 0:
                    missing_pilots.append((package, flight))

        if not missing_pilots:
            return False

        formatted = "<br />".join(
            [f"{p.primary_task} {p.target}: {f}" for p, f in missing_pilots]
        )
        mbox = QMessageBox(
            QMessageBox.Critical,
            "Flights are missing pilots",
            (
                "The following flights are missing one or more pilots:<br />"
                "<br />"
                f"{formatted}<br />"
                "<br />"
                "You must either assign pilots to those flights or cancel those "
                "missions."
            ),
            parent=self,
        )
        mbox.setEscapeButton(mbox.addButton(QMessageBox.Close))
        mbox.exec_()
        return True

    def check_valid_autoresolve_settings(self) -> bool:
        if not self.game.settings.fast_forward_to_first_contact:
            return True

        if not self.game.settings.auto_resolve_combat:
            return True

        has_clients = self.ato_has_clients()
        if (
            has_clients
            and self.game.settings.player_mission_interrupts_sim_at is not None
        ):
            return True

        if has_clients:
            message = textwrap.dedent(
                """\
                You have enabled settings to fast forward and to auto-resolve combat,
                but have not selected any interrupt condition. Fast forward will never
                stop with your current settings. To use auto- resolve, you must choose a
                "Player missions interrupt fast forward" setting other than "Never".
                """
            )
        else:
            message = textwrap.dedent(
                """\
                You have enabled settings to fast forward and to auto-resolve combat,
                but have no players. Fast forward will never stop with your current
                settings. Auto-resolve and fast forward cannot be used without player
                flights and a "Player missions interrupt fast forward" setting other
                than "Never".
                """
            )

        mbox = QMessageBox(
            QMessageBox.Icon.Critical,
            "Incompatible fast-forward settings",
            message,
            parent=self,
        )
        mbox.setEscapeButton(mbox.addButton(QMessageBox.StandardButton.Close))
        mbox.exec()
        return False

    def launch_mission(self):
        """Finishes planning and waits for mission completion."""
        if not self.ato_has_clients() and not self.confirm_no_client_launch():
            return

        if self.check_no_missing_pilots():
            return

        negative_starts = self.negative_start_packages(
            self.sim_controller.current_time_in_sim
        )
        if negative_starts:
            if not self.confirm_negative_start_time(negative_starts):
                return

        if not self.check_valid_autoresolve_settings():
            return

        if self.game.settings.fast_forward_to_first_contact:
            with logged_duration("Simulating to first contact"):
                self.sim_controller.run_to_first_contact()
        self.sim_controller.generate_miz(
            persistence.mission_path_for("liberation_nextturn.miz")
        )

        waiting = QWaitingForMissionResultWindow(
            self.game, self.sim_controller, self.reset_to_pre_sim_checkpoint, self
        )
        waiting.exec_()

    def budget_update(self, game: Game):
        self.budgetBox.setGame(game)
