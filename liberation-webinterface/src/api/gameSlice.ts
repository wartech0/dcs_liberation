import { RootState } from "../app/store";
import { gameLoaded, gameUnloaded } from "./actions";
import { createSlice } from "@reduxjs/toolkit";

interface GameState {
  current_income: number;
}

const initialState: GameState = {
  current_income: 0,
};

const gameSlice = createSlice({
  name: "game_state",
  initialState: initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder.addCase(gameLoaded, (state, action) => {
      if (action.payload.current_income != null) {
        state.current_income = action.payload.current_income;
      }
    });
    builder.addCase(gameUnloaded, (state) => {
      state.current_income = 0;
    });
  },
});

export const getCurrentIncome = (state: RootState) => state.gameState.current_income;

export default gameSlice.reducer;