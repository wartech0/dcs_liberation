import axios from "axios";

//TODO: add a configuration file for this
const backendAddr = "127.0.0.1:16880";

// MSW can't handle IPv6 URLs...
// https://github.com/mswjs/msw/issues/1388
export const HTTP_URL =
  process.env.NODE_ENV === "test" ? "" : `http://${backendAddr}/`;

export const backend = axios.create({
  baseURL: HTTP_URL,
});

export const WEBSOCKET_URL = `ws://${backendAddr}/eventstream`;

export default backend;
