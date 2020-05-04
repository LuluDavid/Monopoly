function getBoxesPositions(L) {
    var l = L / 12.25
    var h = l * 1.625

    var axCoords = {
      0: 0,
      1: (h+l)/2,
      2: (h+3*l)/2,
      3: (h+5*l)/2,
      4: (h+7*l)/2,
      5: (h+9*l)/2,
      6: L-(3*h+7*l)/2,
      7: L-(3*h+5*l)/2,
      8: L-(3*h+3*l)/2,
      9: L-(3*h+l)/2,
      10: L-h
    }

    positions = {
        0: {x: axCoords[0], y: axCoords[0]},
        1: {x: axCoords[0], y: axCoords[1]},
        2: {x: axCoords[0], y: axCoords[2]},
        3: {x: axCoords[0], y: axCoords[3]},
        4: {x: axCoords[0], y: axCoords[4]},
        5: {x: axCoords[0], y: axCoords[5]},
        6: {x: axCoords[0], y: axCoords[6]},
        7: {x: axCoords[0], y: axCoords[7]},
        8: {x: axCoords[0], y: axCoords[8]},
        9: {x: axCoords[0], y: axCoords[9]},
        10: {x: axCoords[0], y: axCoords[10]},
        11: {x: axCoords[1], y: axCoords[10]},
        12: {x: axCoords[2], y: axCoords[10]},
        13: {x: axCoords[3], y: axCoords[10]},
        14: {x: axCoords[4], y: axCoords[10]},
        15: {x: axCoords[5], y: axCoords[10]},
        16: {x: axCoords[6], y: axCoords[10]},
        17: {x: axCoords[7], y: axCoords[10]},
        18: {x: axCoords[8], y: axCoords[10]},
        19: {x: axCoords[9], y: axCoords[10]},
        20: {x: axCoords[10], y: axCoords[10]},
        21: {x: axCoords[10], y: axCoords[9]},
        22: {x: axCoords[10], y: axCoords[8]},
        23: {x: axCoords[10], y: axCoords[7]},
        24: {x: axCoords[10], y: axCoords[6]},
        25: {x: axCoords[10], y: axCoords[5]},
        26: {x: axCoords[10], y: axCoords[4]},
        27: {x: axCoords[10], y: axCoords[3]},
        28: {x: axCoords[10], y: axCoords[2]},
        29: {x: axCoords[10], y: axCoords[1]},
        30: {x: axCoords[10], y: axCoords[0]},
        31: {x: axCoords[9], y: axCoords[0]},
        32: {x: axCoords[8], y: axCoords[0]},
        33: {x: axCoords[7], y: axCoords[0]},
        34: {x: axCoords[6], y: axCoords[0]},
        35: {x: axCoords[5], y: axCoords[0]},
        36: {x: axCoords[4], y: axCoords[0]},
        37: {x: axCoords[3], y: axCoords[0]},
        38: {x: axCoords[2], y: axCoords[0]},
        39: {x: axCoords[1], y: axCoords[0]}
    };
  return positions;
}
