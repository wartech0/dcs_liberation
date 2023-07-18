import { gameLoaded, gameUnloaded } from "./actions";
import { ControlPoint, Tgo } from "./liberationApi";
import { PayloadAction, createSlice } from "@reduxjs/toolkit";

interface WebInterfaceState {
  selectedControlPoint: ControlPoint | null;
  selectedTgo: Tgo | null;
  Tgo: boolean;
  ControlPoint: boolean;
}

const initialState: WebInterfaceState = {
  selectedControlPoint: null,
  selectedTgo: null,
  Tgo: false,
  ControlPoint: false
};

export const webInterfaceSlice = createSlice({
  name: "webInterface",
  initialState,
  reducers: {
    selectInterfaceCP: (state, action: PayloadAction<ControlPoint>) => {
        state.selectedControlPoint = action.payload;
        state.ControlPoint = true;
        state.Tgo = false;
      },
    selectInterfaceTgo: (state, action: PayloadAction<Tgo>) => {
        state.selectedTgo = action.payload;
        state.Tgo = true;
        state.ControlPoint = false;
    }
  },
  extraReducers: (builder) => {
    builder.addCase(gameLoaded, (state, action) => {
      state.selectedControlPoint = null;
      state.selectedTgo = null;
      state.Tgo = false;
      state.ControlPoint = false;
    });
    builder.addCase(gameUnloaded, (state) => {
        state.selectedControlPoint = null;
        state.selectedTgo = null;
        state.Tgo = false;
        state.ControlPoint = false;
    });
  },
});

export const {
    selectInterfaceCP,
    selectInterfaceTgo
} = webInterfaceSlice.actions;


export default webInterfaceSlice.reducer;
