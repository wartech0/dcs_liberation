import { RootState } from "../app/store";
import { gameLoaded, gameUnloaded } from "./actions";
import { Package } from "./_liberationApi";
import { PayloadAction, createSlice } from "@reduxjs/toolkit";

interface Packages {
  packages: {[key: string]:Package}
}

const initialState: Packages = {
  packages: {},
};

const packagesSlice = createSlice({
  name: "packages",
  initialState: initialState,
  reducers: {
    newPackages: (state, action: PayloadAction<Package[]>) => {
        for (const pack of action.payload) {
          state.packages[pack.id] = pack;
        }
      },
      updatePackages: (state, action: PayloadAction<Package[]>) => {
        for (const pack of action.payload) {
          state.packages[pack.id] = pack;
        }
      },
      deletePackages: (state, action: PayloadAction<string[]>) => {
        for (const cID of action.payload) {
          delete state.packages[cID];
        }
      },
  },
  extraReducers: (builder) => {
    builder.addCase(gameLoaded, (state, action) => {
        state.packages = action.payload.packages.reduce(
          (acc: { [key: string]: Package }, curr) => {
            acc[curr.id] = curr;
            return acc;
          },
          {}
        );
      });
      builder.addCase(gameUnloaded, (state) => {
        state.packages = {};
      });
    },
});

export const { newPackages, updatePackages, deletePackages } =
  packagesSlice.actions;
export const getPackages = (state: RootState) => state.packagesState.packages;

export default packagesSlice.reducer;