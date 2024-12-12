// src/recoil/atoms.js
import { atom } from 'recoil';

export const videoFeed1State = atom({
  key: 'videoFeed1State',
  default: null,
});

export const outputDataState = atom({
  key: 'outputDataState',
  default: [],
});

export const videoRefsAtom = atom({
  key: 'videoRefsAtom',
  default: {
    videoFeed1: null,
  },
});

export const mainImageState = atom({
  key: 'mainImageState',
  default: {
    image: null,
    classes: [],
    boundingBoxes: [],
  },
});