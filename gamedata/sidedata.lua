local sideData = {
  [1] = {
    name      = 'ARM',
    startunit = 'arm_commander',
	startunitai = 'arm_commander',
	uiSets = {
		Main	= {0.40, 0.20, 0.70, 1},
		Trim	= {1.00, 0.80, 0.00, 1},
		Rank	= {1.00, 0.90, 0.50, 1},
	},
  },
  [2] = {
    name      = 'CORE',
    startunit = 'core_commander',
	startunitai = 'core_commander',
	uiSets = {
		Main	= {0.40, 0.20, 0.70, 1},
		Trim	= {1.00, 0.80, 0.00, 1},
		Rank	= {1.00, 0.90, 0.50, 1},
	},
  },
}
return sideData