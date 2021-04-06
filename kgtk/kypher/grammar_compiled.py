def createParserClass(GrammarBase, ruleGlobals):
    if ruleGlobals is None:
        ruleGlobals = {}
    class Grammar(GrammarBase):
        def rule_Kypher(self):
            _locals = {'self': self}
            self.locals['Kypher'] = _locals
            self._trace('er ', (9, 12), self.input.position)
            _G_apply_1, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'Kypher')
            self._trace('= WS State', (12, 22), self.input.position)
            _G_apply_2, lastError = self._apply(self.rule_Statement, "Statement", [])
            self.considerError(lastError, 'Kypher')
            _locals['s'] = _G_apply_2
            def _G_optional_3():
                self._trace(':s', (26, 28), self.input.position)
                _G_apply_4, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace(' (WS', (28, 32), self.input.position)
                _G_exactly_5, lastError = self.exactly(';')
                self.considerError(lastError, None)
                return (_G_exactly_5, self.currentError)
            def _G_optional_6():
                return (None, self.input.nullError())
            _G_or_7, lastError = self._or([_G_optional_3, _G_optional_6])
            self.considerError(lastError, 'Kypher')
            self._trace(";')", (34, 37), self.input.position)
            _G_apply_8, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'Kypher')
            _G_python_10, lastError = eval(self._G_expr_9, self.globals, _locals), None
            self.considerError(lastError, 'Kypher')
            return (_G_python_10, self.currentError)


        def rule_Statement(self):
            _locals = {'self': self}
            self.locals['Statement'] = _locals
            self._trace('tement', (55, 61), self.input.position)
            _G_apply_11, lastError = self._apply(self.rule_Query, "Query", [])
            self.considerError(lastError, 'Statement')
            return (_G_apply_11, self.currentError)


        def rule_Query(self):
            _locals = {'self': self}
            self.locals['Query'] = _locals
            self._trace('\n    Query = ', (70, 83), self.input.position)
            _G_apply_12, lastError = self._apply(self.rule_RegularQuery, "RegularQuery", [])
            self.considerError(lastError, 'Query')
            return (_G_apply_12, self.currentError)


        def rule_RegularQuery(self):
            _locals = {'self': self}
            self.locals['RegularQuery'] = _locals
            def _G_or_13():
                self._trace('  RegularQue', (99, 111), self.input.position)
                _G_apply_14, lastError = self._apply(self.rule_SingleQuery, "SingleQuery", [])
                self.considerError(lastError, None)
                _locals['sq'] = _G_apply_14
                self._trace('= S', (114, 117), self.input.position)
                _G_apply_15, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('in', (117, 119), self.input.position)
                _G_apply_16, lastError = self._apply(self.rule_U, "U", [])
                self.considerError(lastError, None)
                self._trace('gl', (119, 121), self.input.position)
                _G_apply_17, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace('eQ', (121, 123), self.input.position)
                _G_apply_18, lastError = self._apply(self.rule_I, "I", [])
                self.considerError(lastError, None)
                self._trace('ue', (123, 125), self.input.position)
                _G_apply_19, lastError = self._apply(self.rule_O, "O", [])
                self.considerError(lastError, None)
                self._trace('ry', (125, 127), self.input.position)
                _G_apply_20, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace(':sq', (127, 130), self.input.position)
                _G_apply_21, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace(' S', (130, 132), self.input.position)
                _G_apply_22, lastError = self._apply(self.rule_A, "A", [])
                self.considerError(lastError, None)
                self._trace('P ', (132, 134), self.input.position)
                _G_apply_23, lastError = self._apply(self.rule_L, "L", [])
                self.considerError(lastError, None)
                self._trace('U ', (134, 136), self.input.position)
                _G_apply_24, lastError = self._apply(self.rule_L, "L", [])
                self.considerError(lastError, None)
                self._trace('N I', (136, 139), self.input.position)
                _G_apply_25, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace(' O N SP A L L', (139, 152), self.input.position)
                _G_apply_26, lastError = self._apply(self.rule_RegularQuery, "RegularQuery", [])
                self.considerError(lastError, None)
                _locals['rq'] = _G_apply_26
                _G_python_28, lastError = eval(self._G_expr_27, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_28, self.currentError)
            def _G_or_29():
                self._trace(']\n          ', (194, 206), self.input.position)
                _G_apply_30, lastError = self._apply(self.rule_SingleQuery, "SingleQuery", [])
                self.considerError(lastError, None)
                _locals['sq'] = _G_apply_30
                self._trace('   ', (209, 212), self.input.position)
                _G_apply_31, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace(' |', (212, 214), self.input.position)
                _G_apply_32, lastError = self._apply(self.rule_U, "U", [])
                self.considerError(lastError, None)
                self._trace(' S', (214, 216), self.input.position)
                _G_apply_33, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace('in', (216, 218), self.input.position)
                _G_apply_34, lastError = self._apply(self.rule_I, "I", [])
                self.considerError(lastError, None)
                self._trace('gl', (218, 220), self.input.position)
                _G_apply_35, lastError = self._apply(self.rule_O, "O", [])
                self.considerError(lastError, None)
                self._trace('eQ', (220, 222), self.input.position)
                _G_apply_36, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace('uer', (222, 225), self.input.position)
                _G_apply_37, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('y:sq SP U N I', (225, 238), self.input.position)
                _G_apply_38, lastError = self._apply(self.rule_RegularQuery, "RegularQuery", [])
                self.considerError(lastError, None)
                _locals['rq'] = _G_apply_38
                _G_python_40, lastError = eval(self._G_expr_39, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_40, self.currentError)
            def _G_or_41():
                self._trace(', rq]\n      ', (277, 289), self.input.position)
                _G_apply_42, lastError = self._apply(self.rule_SingleQuery, "SingleQuery", [])
                self.considerError(lastError, None)
                _locals['sq'] = _G_apply_42
                return (_G_apply_42, self.currentError)
            _G_or_43, lastError = self._or([_G_or_13, _G_or_29, _G_or_41])
            self.considerError(lastError, 'RegularQuery')
            return (_G_or_43, self.currentError)


        def rule_SingleQuery(self):
            _locals = {'self': self}
            self.locals['SingleQuery'] = _locals
            def _G_optional_44():
                self._trace(' Remov', (544, 550), self.input.position)
                _G_apply_45, lastError = self._apply(self.rule_Match, "Match", [])
                self.considerError(lastError, None)
                return (_G_apply_45, self.currentError)
            def _G_optional_46():
                return (None, self.input.nullError())
            _G_or_47, lastError = self._or([_G_optional_44, _G_optional_46])
            self.considerError(lastError, 'SingleQuery')
            _locals['m'] = _G_or_47
            self._trace('   ', (553, 556), self.input.position)
            _G_apply_48, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'SingleQuery')
            def _G_optional_49():
                self._trace('#    ', (556, 561), self.input.position)
                _G_apply_50, lastError = self._apply(self.rule_With, "With", [])
                self.considerError(lastError, None)
                return (_G_apply_50, self.currentError)
            def _G_optional_51():
                return (None, self.input.nullError())
            _G_or_52, lastError = self._or([_G_optional_49, _G_optional_51])
            self.considerError(lastError, 'SingleQuery')
            _locals['w'] = _G_or_52
            self._trace(' | ', (564, 567), self.input.position)
            _G_apply_53, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'SingleQuery')
            self._trace('With\n  ', (567, 574), self.input.position)
            _G_apply_54, lastError = self._apply(self.rule_Return, "Return", [])
            self.considerError(lastError, 'SingleQuery')
            _locals['r'] = _G_apply_54
            _G_python_56, lastError = eval(self._G_expr_55, self.globals, _locals), None
            self.considerError(lastError, 'SingleQuery')
            return (_G_python_56, self.currentError)


        def rule_StrictMatch(self):
            _locals = {'self': self}
            self.locals['StrictMatch'] = _locals
            self._trace(':m', (619, 621), self.input.position)
            _G_apply_57, lastError = self._apply(self.rule_M, "M", [])
            self.considerError(lastError, 'StrictMatch')
            self._trace(' W', (621, 623), self.input.position)
            _G_apply_58, lastError = self._apply(self.rule_A, "A", [])
            self.considerError(lastError, 'StrictMatch')
            self._trace('S ', (623, 625), self.input.position)
            _G_apply_59, lastError = self._apply(self.rule_T, "T", [])
            self.considerError(lastError, 'StrictMatch')
            self._trace('Wi', (625, 627), self.input.position)
            _G_apply_60, lastError = self._apply(self.rule_C, "C", [])
            self.considerError(lastError, 'StrictMatch')
            self._trace('th', (627, 629), self.input.position)
            _G_apply_61, lastError = self._apply(self.rule_H, "H", [])
            self.considerError(lastError, 'StrictMatch')
            self._trace('?:w', (629, 632), self.input.position)
            _G_apply_62, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'StrictMatch')
            self._trace(' WS Retu', (632, 640), self.input.position)
            _G_apply_63, lastError = self._apply(self.rule_Pattern, "Pattern", [])
            self.considerError(lastError, 'StrictMatch')
            _locals['p'] = _G_apply_63
            def _G_optional_64():
                self._trace(' -', (644, 646), self.input.position)
                _G_apply_65, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('> ["Si', (646, 652), self.input.position)
                _G_apply_66, lastError = self._apply(self.rule_Where, "Where", [])
                self.considerError(lastError, None)
                return (_G_apply_66, self.currentError)
            def _G_optional_67():
                return (None, self.input.nullError())
            _G_or_68, lastError = self._or([_G_optional_64, _G_optional_67])
            self.considerError(lastError, 'StrictMatch')
            _locals['w'] = _G_or_68
            _G_python_70, lastError = eval(self._G_expr_69, self.globals, _locals), None
            self.considerError(lastError, 'StrictMatch')
            return (_G_python_70, self.currentError)


        def rule_OptionalMatch(self):
            _locals = {'self': self}
            self.locals['OptionalMatch'] = _locals
            self._trace('C ', (698, 700), self.input.position)
            _G_apply_71, lastError = self._apply(self.rule_O, "O", [])
            self.considerError(lastError, 'OptionalMatch')
            self._trace('H ', (700, 702), self.input.position)
            _G_apply_72, lastError = self._apply(self.rule_P, "P", [])
            self.considerError(lastError, 'OptionalMatch')
            self._trace('WS', (702, 704), self.input.position)
            _G_apply_73, lastError = self._apply(self.rule_T, "T", [])
            self.considerError(lastError, 'OptionalMatch')
            self._trace(' P', (704, 706), self.input.position)
            _G_apply_74, lastError = self._apply(self.rule_I, "I", [])
            self.considerError(lastError, 'OptionalMatch')
            self._trace('at', (706, 708), self.input.position)
            _G_apply_75, lastError = self._apply(self.rule_O, "O", [])
            self.considerError(lastError, 'OptionalMatch')
            self._trace('te', (708, 710), self.input.position)
            _G_apply_76, lastError = self._apply(self.rule_N, "N", [])
            self.considerError(lastError, 'OptionalMatch')
            self._trace('rn', (710, 712), self.input.position)
            _G_apply_77, lastError = self._apply(self.rule_A, "A", [])
            self.considerError(lastError, 'OptionalMatch')
            self._trace(':p', (712, 714), self.input.position)
            _G_apply_78, lastError = self._apply(self.rule_L, "L", [])
            self.considerError(lastError, 'OptionalMatch')
            self._trace(' (W', (714, 717), self.input.position)
            _G_apply_79, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'OptionalMatch')
            self._trace('S ', (717, 719), self.input.position)
            _G_apply_80, lastError = self._apply(self.rule_M, "M", [])
            self.considerError(lastError, 'OptionalMatch')
            self._trace('Wh', (719, 721), self.input.position)
            _G_apply_81, lastError = self._apply(self.rule_A, "A", [])
            self.considerError(lastError, 'OptionalMatch')
            self._trace('er', (721, 723), self.input.position)
            _G_apply_82, lastError = self._apply(self.rule_T, "T", [])
            self.considerError(lastError, 'OptionalMatch')
            self._trace('e)', (723, 725), self.input.position)
            _G_apply_83, lastError = self._apply(self.rule_C, "C", [])
            self.considerError(lastError, 'OptionalMatch')
            self._trace('?:', (725, 727), self.input.position)
            _G_apply_84, lastError = self._apply(self.rule_H, "H", [])
            self.considerError(lastError, 'OptionalMatch')
            self._trace('w -', (727, 730), self.input.position)
            _G_apply_85, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'OptionalMatch')
            self._trace('> ["Stri', (730, 738), self.input.position)
            _G_apply_86, lastError = self._apply(self.rule_Pattern, "Pattern", [])
            self.considerError(lastError, 'OptionalMatch')
            _locals['p'] = _G_apply_86
            def _G_optional_87():
                self._trace('tc', (742, 744), self.input.position)
                _G_apply_88, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('h", p,', (744, 750), self.input.position)
                _G_apply_89, lastError = self._apply(self.rule_Where, "Where", [])
                self.considerError(lastError, None)
                return (_G_apply_89, self.currentError)
            def _G_optional_90():
                return (None, self.input.nullError())
            _G_or_91, lastError = self._or([_G_optional_87, _G_optional_90])
            self.considerError(lastError, 'OptionalMatch')
            _locals['w'] = _G_or_91
            _G_python_93, lastError = eval(self._G_expr_92, self.globals, _locals), None
            self.considerError(lastError, 'OptionalMatch')
            return (_G_python_93, self.currentError)


        def rule_Match(self):
            _locals = {'self': self}
            self.locals['Match'] = _locals
            self._trace('xactly one s', (888, 900), self.input.position)
            _G_apply_94, lastError = self._apply(self.rule_StrictMatch, "StrictMatch", [])
            self.considerError(lastError, 'Match')
            _locals['head'] = _G_apply_94
            def _G_many_95():
                self._trace('at', (907, 909), self.input.position)
                _G_apply_96, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('ch and zero or', (909, 923), self.input.position)
                _G_apply_97, lastError = self._apply(self.rule_OptionalMatch, "OptionalMatch", [])
                self.considerError(lastError, None)
                return (_G_apply_97, self.currentError)
            _G_many_98, lastError = self.many(_G_many_95)
            self.considerError(lastError, 'Match')
            _locals['tail'] = _G_many_98
            _G_python_100, lastError = eval(self._G_expr_99, self.globals, _locals), None
            self.considerError(lastError, 'Match')
            return (_G_python_100, self.currentError)


        def rule_Unwind(self):
            _locals = {'self': self}
            self.locals['Unwind'] = _locals
            self._trace('at', (966, 968), self.input.position)
            _G_apply_101, lastError = self._apply(self.rule_U, "U", [])
            self.considerError(lastError, 'Unwind')
            self._trace('ch', (968, 970), self.input.position)
            _G_apply_102, lastError = self._apply(self.rule_N, "N", [])
            self.considerError(lastError, 'Unwind')
            self._trace(' =', (970, 972), self.input.position)
            _G_apply_103, lastError = self._apply(self.rule_W, "W", [])
            self.considerError(lastError, 'Unwind')
            self._trace(' S', (972, 974), self.input.position)
            _G_apply_104, lastError = self._apply(self.rule_I, "I", [])
            self.considerError(lastError, 'Unwind')
            self._trace('tr', (974, 976), self.input.position)
            _G_apply_105, lastError = self._apply(self.rule_N, "N", [])
            self.considerError(lastError, 'Unwind')
            self._trace('ic', (976, 978), self.input.position)
            _G_apply_106, lastError = self._apply(self.rule_D, "D", [])
            self.considerError(lastError, 'Unwind')
            self._trace('tMa', (978, 981), self.input.position)
            _G_apply_107, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'Unwind')
            self._trace('tch:head (W', (981, 992), self.input.position)
            _G_apply_108, lastError = self._apply(self.rule_Expression, "Expression", [])
            self.considerError(lastError, 'Unwind')
            _locals['ex'] = _G_apply_108
            self._trace('pti', (995, 998), self.input.position)
            _G_apply_109, lastError = self._apply(self.rule_SP, "SP", [])
            self.considerError(lastError, 'Unwind')
            self._trace('on', (998, 1000), self.input.position)
            _G_apply_110, lastError = self._apply(self.rule_A, "A", [])
            self.considerError(lastError, 'Unwind')
            self._trace('al', (1000, 1002), self.input.position)
            _G_apply_111, lastError = self._apply(self.rule_S, "S", [])
            self.considerError(lastError, 'Unwind')
            self._trace('Mat', (1002, 1005), self.input.position)
            _G_apply_112, lastError = self._apply(self.rule_SP, "SP", [])
            self.considerError(lastError, 'Unwind')
            self._trace('ch)*:tail', (1005, 1014), self.input.position)
            _G_apply_113, lastError = self._apply(self.rule_Variable, "Variable", [])
            self.considerError(lastError, 'Unwind')
            _locals['v'] = _G_apply_113
            _G_python_115, lastError = eval(self._G_expr_114, self.globals, _locals), None
            self.considerError(lastError, 'Unwind')
            return (_G_python_115, self.currentError)


        def rule_Merge(self):
            _locals = {'self': self}
            self.locals['Merge'] = _locals
            self._trace('Un', (1046, 1048), self.input.position)
            _G_apply_116, lastError = self._apply(self.rule_M, "M", [])
            self.considerError(lastError, 'Merge')
            self._trace('wi', (1048, 1050), self.input.position)
            _G_apply_117, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'Merge')
            self._trace('nd', (1050, 1052), self.input.position)
            _G_apply_118, lastError = self._apply(self.rule_R, "R", [])
            self.considerError(lastError, 'Merge')
            self._trace(' =', (1052, 1054), self.input.position)
            _G_apply_119, lastError = self._apply(self.rule_G, "G", [])
            self.considerError(lastError, 'Merge')
            self._trace(' U', (1054, 1056), self.input.position)
            _G_apply_120, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'Merge')
            self._trace(' N ', (1056, 1059), self.input.position)
            _G_apply_121, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'Merge')
            self._trace('W I N D WS E', (1059, 1071), self.input.position)
            _G_apply_122, lastError = self._apply(self.rule_PatternPart, "PatternPart", [])
            self.considerError(lastError, 'Merge')
            _locals['head'] = _G_apply_122
            def _G_many_123():
                self._trace('on', (1078, 1080), self.input.position)
                _G_apply_124, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace(':ex SP A S S', (1080, 1092), self.input.position)
                _G_apply_125, lastError = self._apply(self.rule_MergeAction, "MergeAction", [])
                self.considerError(lastError, None)
                return (_G_apply_125, self.currentError)
            _G_many_126, lastError = self.many(_G_many_123)
            self.considerError(lastError, 'Merge')
            _locals['tail'] = _G_many_126
            _G_python_128, lastError = eval(self._G_expr_127, self.globals, _locals), None
            self.considerError(lastError, 'Merge')
            return (_G_python_128, self.currentError)


        def rule_MergeAction(self):
            _locals = {'self': self}
            self.locals['MergeAction'] = _locals
            def _G_or_129():
                self._trace(' R', (1142, 1144), self.input.position)
                _G_apply_130, lastError = self._apply(self.rule_O, "O", [])
                self.considerError(lastError, None)
                self._trace(' G', (1144, 1146), self.input.position)
                _G_apply_131, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace(' E ', (1146, 1149), self.input.position)
                _G_apply_132, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('WS', (1149, 1151), self.input.position)
                _G_apply_133, lastError = self._apply(self.rule_M, "M", [])
                self.considerError(lastError, None)
                self._trace(' P', (1151, 1153), self.input.position)
                _G_apply_134, lastError = self._apply(self.rule_A, "A", [])
                self.considerError(lastError, None)
                self._trace('at', (1153, 1155), self.input.position)
                _G_apply_135, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                self._trace('te', (1155, 1157), self.input.position)
                _G_apply_136, lastError = self._apply(self.rule_C, "C", [])
                self.considerError(lastError, None)
                self._trace('rn', (1157, 1159), self.input.position)
                _G_apply_137, lastError = self._apply(self.rule_H, "H", [])
                self.considerError(lastError, None)
                self._trace('Par', (1159, 1162), self.input.position)
                _G_apply_138, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('t:he', (1162, 1166), self.input.position)
                _G_apply_139, lastError = self._apply(self.rule_Set, "Set", [])
                self.considerError(lastError, None)
                _locals['s'] = _G_apply_139
                _G_python_141, lastError = eval(self._G_expr_140, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_141, self.currentError)
            def _G_or_142():
                self._trace('d]', (1209, 1211), self.input.position)
                _G_apply_143, lastError = self._apply(self.rule_O, "O", [])
                self.considerError(lastError, None)
                self._trace(' +', (1211, 1213), self.input.position)
                _G_apply_144, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace(' ta', (1213, 1216), self.input.position)
                _G_apply_145, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('il', (1216, 1218), self.input.position)
                _G_apply_146, lastError = self._apply(self.rule_C, "C", [])
                self.considerError(lastError, None)
                self._trace(']\n', (1218, 1220), self.input.position)
                _G_apply_147, lastError = self._apply(self.rule_R, "R", [])
                self.considerError(lastError, None)
                self._trace('\n ', (1220, 1222), self.input.position)
                _G_apply_148, lastError = self._apply(self.rule_E, "E", [])
                self.considerError(lastError, None)
                self._trace('  ', (1222, 1224), self.input.position)
                _G_apply_149, lastError = self._apply(self.rule_A, "A", [])
                self.considerError(lastError, None)
                self._trace(' M', (1224, 1226), self.input.position)
                _G_apply_150, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                self._trace('er', (1226, 1228), self.input.position)
                _G_apply_151, lastError = self._apply(self.rule_E, "E", [])
                self.considerError(lastError, None)
                self._trace('geA', (1228, 1231), self.input.position)
                _G_apply_152, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('ctio', (1231, 1235), self.input.position)
                _G_apply_153, lastError = self._apply(self.rule_Set, "Set", [])
                self.considerError(lastError, None)
                _locals['s'] = _G_apply_153
                _G_python_155, lastError = eval(self._G_expr_154, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_155, self.currentError)
            _G_or_156, lastError = self._or([_G_or_129, _G_or_142])
            self.considerError(lastError, 'MergeAction')
            return (_G_or_156, self.currentError)


        def rule_Create(self):
            _locals = {'self': self}
            self.locals['Create'] = _locals
            self._trace('Ac', (1275, 1277), self.input.position)
            _G_apply_157, lastError = self._apply(self.rule_C, "C", [])
            self.considerError(lastError, 'Create')
            self._trace('ti', (1277, 1279), self.input.position)
            _G_apply_158, lastError = self._apply(self.rule_R, "R", [])
            self.considerError(lastError, 'Create')
            self._trace('on', (1279, 1281), self.input.position)
            _G_apply_159, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'Create')
            self._trace('Ma', (1281, 1283), self.input.position)
            _G_apply_160, lastError = self._apply(self.rule_A, "A", [])
            self.considerError(lastError, 'Create')
            self._trace('tc', (1283, 1285), self.input.position)
            _G_apply_161, lastError = self._apply(self.rule_T, "T", [])
            self.considerError(lastError, 'Create')
            self._trace('h"', (1285, 1287), self.input.position)
            _G_apply_162, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'Create')
            self._trace(', s', (1287, 1290), self.input.position)
            _G_apply_163, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'Create')
            self._trace(']\n      ', (1290, 1298), self.input.position)
            _G_apply_164, lastError = self._apply(self.rule_Pattern, "Pattern", [])
            self.considerError(lastError, 'Create')
            _locals['p'] = _G_apply_164
            _G_python_166, lastError = eval(self._G_expr_165, self.globals, _locals), None
            self.considerError(lastError, 'Create')
            return (_G_python_166, self.currentError)


        def rule_Set(self):
            _locals = {'self': self}
            self.locals['Set'] = _locals
            self._trace(' T', (1324, 1326), self.input.position)
            _G_apply_167, lastError = self._apply(self.rule_S, "S", [])
            self.considerError(lastError, 'Set')
            self._trace(' E', (1326, 1328), self.input.position)
            _G_apply_168, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'Set')
            self._trace(' S', (1328, 1330), self.input.position)
            _G_apply_169, lastError = self._apply(self.rule_T, "T", [])
            self.considerError(lastError, 'Set')
            self._trace('P S', (1330, 1333), self.input.position)
            _G_apply_170, lastError = self._apply(self.rule_SP, "SP", [])
            self.considerError(lastError, 'Set')
            self._trace('et:s -> ', (1333, 1341), self.input.position)
            _G_apply_171, lastError = self._apply(self.rule_SetItem, "SetItem", [])
            self.considerError(lastError, 'Set')
            _locals['head'] = _G_apply_171
            def _G_many_172():
                self._trace('Ac', (1348, 1350), self.input.position)
                _G_apply_173, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('tion', (1350, 1354), self.input.position)
                _G_exactly_174, lastError = self.exactly(',')
                self.considerError(lastError, None)
                self._trace('Cre', (1354, 1357), self.input.position)
                _G_apply_175, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('ate", s]', (1357, 1365), self.input.position)
                _G_apply_176, lastError = self._apply(self.rule_SetItem, "SetItem", [])
                self.considerError(lastError, None)
                return (_G_apply_176, self.currentError)
            _G_many_177, lastError = self.many(_G_many_172)
            self.considerError(lastError, 'Set')
            _locals['tail'] = _G_many_177
            _G_python_179, lastError = eval(self._G_expr_178, self.globals, _locals), None
            self.considerError(lastError, 'Set')
            return (_G_python_179, self.currentError)


        def rule_SetItem(self):
            _locals = {'self': self}
            self.locals['SetItem'] = _locals
            def _G_or_180():
                self._trace('"Create", p]\n\n    S', (1409, 1428), self.input.position)
                _G_apply_181, lastError = self._apply(self.rule_PropertyExpression, "PropertyExpression", [])
                self.considerError(lastError, None)
                _locals['pex'] = _G_apply_181
                self._trace(' S E', (1432, 1436), self.input.position)
                _G_exactly_182, lastError = self.exactly('=')
                self.considerError(lastError, None)
                self._trace(' T SP SetIt', (1436, 1447), self.input.position)
                _G_apply_183, lastError = self._apply(self.rule_Expression, "Expression", [])
                self.considerError(lastError, None)
                _locals['ex'] = _G_apply_183
                _G_python_185, lastError = eval(self._G_expr_184, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_185, self.currentError)
            def _G_or_186():
                self._trace('ail]\n\n   ', (1502, 1511), self.input.position)
                _G_apply_187, lastError = self._apply(self.rule_Variable, "Variable", [])
                self.considerError(lastError, None)
                _locals['v'] = _G_apply_187
                self._trace('etIt', (1513, 1517), self.input.position)
                _G_exactly_188, lastError = self.exactly('=')
                self.considerError(lastError, None)
                self._trace('em = Proper', (1517, 1528), self.input.position)
                _G_apply_189, lastError = self._apply(self.rule_Expression, "Expression", [])
                self.considerError(lastError, None)
                _locals['ex'] = _G_apply_189
                _G_python_191, lastError = eval(self._G_expr_190, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_191, self.currentError)
            def _G_or_192():
                self._trace('-> ["SetI', (1563, 1572), self.input.position)
                _G_apply_193, lastError = self._apply(self.rule_Variable, "Variable", [])
                self.considerError(lastError, None)
                _locals['v'] = _G_apply_193
                self._trace('mProp', (1574, 1579), self.input.position)
                _G_exactly_194, lastError = self.exactly('+=')
                self.considerError(lastError, None)
                self._trace('ertyExpress', (1579, 1590), self.input.position)
                _G_apply_195, lastError = self._apply(self.rule_Expression, "Expression", [])
                self.considerError(lastError, None)
                _locals['ex'] = _G_apply_195
                _G_python_196, lastError = eval(self._G_expr_190, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_196, self.currentError)
            def _G_or_197():
                self._trace("le:v '=' ", (1625, 1634), self.input.position)
                _G_apply_198, lastError = self._apply(self.rule_Variable, "Variable", [])
                self.considerError(lastError, None)
                _locals['v'] = _G_apply_198
                self._trace('pression:ex', (1636, 1647), self.input.position)
                _G_apply_199, lastError = self._apply(self.rule_NodeLabels, "NodeLabels", [])
                self.considerError(lastError, None)
                _locals['ex'] = _G_apply_199
                _G_python_200, lastError = eval(self._G_expr_190, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_200, self.currentError)
            _G_or_201, lastError = self._or([_G_or_180, _G_or_186, _G_or_192, _G_or_197])
            self.considerError(lastError, 'SetItem')
            return (_G_or_201, self.currentError)


        def rule_Delete(self):
            _locals = {'self': self}
            self.locals['Delete'] = _locals
            def _G_optional_202():
                self._trace('V', (1684, 1685), self.input.position)
                _G_apply_203, lastError = self._apply(self.rule_D, "D", [])
                self.considerError(lastError, None)
                self._trace('ar', (1685, 1687), self.input.position)
                _G_apply_204, lastError = self._apply(self.rule_E, "E", [])
                self.considerError(lastError, None)
                self._trace('ia', (1687, 1689), self.input.position)
                _G_apply_205, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                self._trace('bl', (1689, 1691), self.input.position)
                _G_apply_206, lastError = self._apply(self.rule_A, "A", [])
                self.considerError(lastError, None)
                self._trace('e:', (1691, 1693), self.input.position)
                _G_apply_207, lastError = self._apply(self.rule_C, "C", [])
                self.considerError(lastError, None)
                self._trace('v ', (1693, 1695), self.input.position)
                _G_apply_208, lastError = self._apply(self.rule_H, "H", [])
                self.considerError(lastError, None)
                self._trace("'+=", (1695, 1698), self.input.position)
                _G_apply_209, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                return (_G_apply_209, self.currentError)
            def _G_optional_210():
                return (None, self.input.nullError())
            _G_or_211, lastError = self._or([_G_optional_202, _G_optional_210])
            self.considerError(lastError, 'Delete')
            self._trace('Ex', (1700, 1702), self.input.position)
            _G_apply_212, lastError = self._apply(self.rule_D, "D", [])
            self.considerError(lastError, 'Delete')
            self._trace('pr', (1702, 1704), self.input.position)
            _G_apply_213, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'Delete')
            self._trace('es', (1704, 1706), self.input.position)
            _G_apply_214, lastError = self._apply(self.rule_L, "L", [])
            self.considerError(lastError, 'Delete')
            self._trace('si', (1706, 1708), self.input.position)
            _G_apply_215, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'Delete')
            self._trace('on', (1708, 1710), self.input.position)
            _G_apply_216, lastError = self._apply(self.rule_T, "T", [])
            self.considerError(lastError, 'Delete')
            self._trace(':e', (1710, 1712), self.input.position)
            _G_apply_217, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'Delete')
            self._trace('x -', (1712, 1715), self.input.position)
            _G_apply_218, lastError = self._apply(self.rule_SP, "SP", [])
            self.considerError(lastError, 'Delete')
            self._trace('> ["SetItem', (1715, 1726), self.input.position)
            _G_apply_219, lastError = self._apply(self.rule_Expression, "Expression", [])
            self.considerError(lastError, 'Delete')
            _locals['head'] = _G_apply_219
            def _G_many_220():
                self._trace('x]\n', (1733, 1736), self.input.position)
                _G_exactly_221, lastError = self.exactly(',')
                self.considerError(lastError, None)
                self._trace('   ', (1736, 1739), self.input.position)
                _G_apply_222, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('         | ', (1739, 1750), self.input.position)
                _G_apply_223, lastError = self._apply(self.rule_Expression, "Expression", [])
                self.considerError(lastError, None)
                return (_G_apply_223, self.currentError)
            _G_many_224, lastError = self.many(_G_many_220)
            self.considerError(lastError, 'Delete')
            _locals['tail'] = _G_many_224
            _G_python_226, lastError = eval(self._G_expr_225, self.globals, _locals), None
            self.considerError(lastError, 'Delete')
            return (_G_python_226, self.currentError)


        def rule_Remove(self):
            _locals = {'self': self}
            self.locals['Remove'] = _locals
            self._trace('\n ', (1797, 1799), self.input.position)
            _G_apply_227, lastError = self._apply(self.rule_R, "R", [])
            self.considerError(lastError, 'Remove')
            self._trace('  ', (1799, 1801), self.input.position)
            _G_apply_228, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'Remove')
            self._trace(' D', (1801, 1803), self.input.position)
            _G_apply_229, lastError = self._apply(self.rule_M, "M", [])
            self.considerError(lastError, 'Remove')
            self._trace('el', (1803, 1805), self.input.position)
            _G_apply_230, lastError = self._apply(self.rule_O, "O", [])
            self.considerError(lastError, 'Remove')
            self._trace('et', (1805, 1807), self.input.position)
            _G_apply_231, lastError = self._apply(self.rule_V, "V", [])
            self.considerError(lastError, 'Remove')
            self._trace('e ', (1807, 1809), self.input.position)
            _G_apply_232, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'Remove')
            self._trace('= (', (1809, 1812), self.input.position)
            _G_apply_233, lastError = self._apply(self.rule_SP, "SP", [])
            self.considerError(lastError, 'Remove')
            self._trace('D E T A C H', (1812, 1823), self.input.position)
            _G_apply_234, lastError = self._apply(self.rule_RemoveItem, "RemoveItem", [])
            self.considerError(lastError, 'Remove')
            _locals['head'] = _G_apply_234
            def _G_many_235():
                self._trace(' E', (1830, 1832), self.input.position)
                _G_apply_236, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace(' L E', (1832, 1836), self.input.position)
                _G_exactly_237, lastError = self.exactly(',')
                self.considerError(lastError, None)
                self._trace(' T ', (1836, 1839), self.input.position)
                _G_apply_238, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('E SP Expres', (1839, 1850), self.input.position)
                _G_apply_239, lastError = self._apply(self.rule_RemoveItem, "RemoveItem", [])
                self.considerError(lastError, None)
                return (_G_apply_239, self.currentError)
            _G_many_240, lastError = self.many(_G_many_235)
            self.considerError(lastError, 'Remove')
            _locals['tail'] = _G_many_240
            _G_python_242, lastError = eval(self._G_expr_241, self.globals, _locals), None
            self.considerError(lastError, 'Remove')
            return (_G_python_242, self.currentError)


        def rule_RemoveItem(self):
            _locals = {'self': self}
            self.locals['RemoveItem'] = _locals
            def _G_or_243():
                self._trace(' [head] +', (1900, 1909), self.input.position)
                _G_apply_244, lastError = self._apply(self.rule_Variable, "Variable", [])
                self.considerError(lastError, None)
                _locals['v'] = _G_apply_244
                self._trace('ail]\n\n    R', (1911, 1922), self.input.position)
                _G_apply_245, lastError = self._apply(self.rule_NodeLabels, "NodeLabels", [])
                self.considerError(lastError, None)
                _locals['nl'] = _G_apply_245
                _G_python_247, lastError = eval(self._G_expr_246, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_247, self.currentError)
            def _G_or_248():
                self._trace("' WS RemoveItem)*:t", (1967, 1986), self.input.position)
                _G_apply_249, lastError = self._apply(self.rule_PropertyExpression, "PropertyExpression", [])
                self.considerError(lastError, None)
                _locals['p'] = _G_apply_249
                _G_python_251, lastError = eval(self._G_expr_250, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_251, self.currentError)
            _G_or_252, lastError = self._or([_G_or_243, _G_or_248])
            self.considerError(lastError, 'RemoveItem')
            return (_G_or_252, self.currentError)


        def rule_With(self):
            _locals = {'self': self}
            self.locals['With'] = _locals
            self._trace('\n ', (2019, 2021), self.input.position)
            _G_apply_253, lastError = self._apply(self.rule_W, "W", [])
            self.considerError(lastError, 'With')
            self._trace('  ', (2021, 2023), self.input.position)
            _G_apply_254, lastError = self._apply(self.rule_I, "I", [])
            self.considerError(lastError, 'With')
            self._trace(' R', (2023, 2025), self.input.position)
            _G_apply_255, lastError = self._apply(self.rule_T, "T", [])
            self.considerError(lastError, 'With')
            self._trace('em', (2025, 2027), self.input.position)
            _G_apply_256, lastError = self._apply(self.rule_H, "H", [])
            self.considerError(lastError, 'With')
            def _G_optional_257():
                self._trace('eI', (2029, 2031), self.input.position)
                _G_apply_258, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('te', (2031, 2033), self.input.position)
                _G_apply_259, lastError = self._apply(self.rule_D, "D", [])
                self.considerError(lastError, None)
                self._trace('m ', (2033, 2035), self.input.position)
                _G_apply_260, lastError = self._apply(self.rule_I, "I", [])
                self.considerError(lastError, None)
                self._trace('= ', (2035, 2037), self.input.position)
                _G_apply_261, lastError = self._apply(self.rule_S, "S", [])
                self.considerError(lastError, None)
                self._trace('Va', (2037, 2039), self.input.position)
                _G_apply_262, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                self._trace('ri', (2039, 2041), self.input.position)
                _G_apply_263, lastError = self._apply(self.rule_I, "I", [])
                self.considerError(lastError, None)
                self._trace('ab', (2041, 2043), self.input.position)
                _G_apply_264, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace('le', (2043, 2045), self.input.position)
                _G_apply_265, lastError = self._apply(self.rule_C, "C", [])
                self.considerError(lastError, None)
                self._trace(':v', (2045, 2047), self.input.position)
                _G_apply_266, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                return (_G_apply_266, self.currentError)
            def _G_optional_267():
                return (None, self.input.nullError())
            _G_or_268, lastError = self._or([_G_optional_257, _G_optional_267])
            self.considerError(lastError, 'With')
            _locals['d'] = _G_or_268
            self._trace('eLa', (2051, 2054), self.input.position)
            _G_apply_269, lastError = self._apply(self.rule_SP, "SP", [])
            self.considerError(lastError, 'With')
            self._trace('bels:nl -> ', (2054, 2065), self.input.position)
            _G_apply_270, lastError = self._apply(self.rule_ReturnBody, "ReturnBody", [])
            self.considerError(lastError, 'With')
            _locals['rb'] = _G_apply_270
            def _G_optional_271():
                self._trace('oveIt', (2070, 2075), self.input.position)
                _G_apply_272, lastError = self._apply(self.rule_Where, "Where", [])
                self.considerError(lastError, None)
                return (_G_apply_272, self.currentError)
            def _G_optional_273():
                return (None, self.input.nullError())
            _G_or_274, lastError = self._or([_G_optional_271, _G_optional_273])
            self.considerError(lastError, 'With')
            _locals['w'] = _G_or_274
            _G_python_276, lastError = eval(self._G_expr_275, self.globals, _locals), None
            self.considerError(lastError, 'With')
            return (_G_python_276, self.currentError)


        def rule_Return(self):
            _locals = {'self': self}
            self.locals['Return'] = _locals
            self._trace('pe', (2111, 2113), self.input.position)
            _G_apply_277, lastError = self._apply(self.rule_R, "R", [])
            self.considerError(lastError, 'Return')
            self._trace('rt', (2113, 2115), self.input.position)
            _G_apply_278, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'Return')
            self._trace('yE', (2115, 2117), self.input.position)
            _G_apply_279, lastError = self._apply(self.rule_T, "T", [])
            self.considerError(lastError, 'Return')
            self._trace('xp', (2117, 2119), self.input.position)
            _G_apply_280, lastError = self._apply(self.rule_U, "U", [])
            self.considerError(lastError, 'Return')
            self._trace('re', (2119, 2121), self.input.position)
            _G_apply_281, lastError = self._apply(self.rule_R, "R", [])
            self.considerError(lastError, 'Return')
            self._trace('ss', (2121, 2123), self.input.position)
            _G_apply_282, lastError = self._apply(self.rule_N, "N", [])
            self.considerError(lastError, 'Return')
            def _G_optional_283():
                self._trace('n:', (2125, 2127), self.input.position)
                _G_apply_284, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('p ', (2127, 2129), self.input.position)
                _G_apply_285, lastError = self._apply(self.rule_D, "D", [])
                self.considerError(lastError, None)
                self._trace('->', (2129, 2131), self.input.position)
                _G_apply_286, lastError = self._apply(self.rule_I, "I", [])
                self.considerError(lastError, None)
                self._trace(' [', (2131, 2133), self.input.position)
                _G_apply_287, lastError = self._apply(self.rule_S, "S", [])
                self.considerError(lastError, None)
                self._trace('"R', (2133, 2135), self.input.position)
                _G_apply_288, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                self._trace('em', (2135, 2137), self.input.position)
                _G_apply_289, lastError = self._apply(self.rule_I, "I", [])
                self.considerError(lastError, None)
                self._trace('ov', (2137, 2139), self.input.position)
                _G_apply_290, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace('eI', (2139, 2141), self.input.position)
                _G_apply_291, lastError = self._apply(self.rule_C, "C", [])
                self.considerError(lastError, None)
                self._trace('te', (2141, 2143), self.input.position)
                _G_apply_292, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                return (_G_apply_292, self.currentError)
            def _G_optional_293():
                return (None, self.input.nullError())
            _G_or_294, lastError = self._or([_G_optional_283, _G_optional_293])
            self.considerError(lastError, 'Return')
            _locals['d'] = _G_or_294
            self._trace(', p', (2147, 2150), self.input.position)
            _G_apply_295, lastError = self._apply(self.rule_SP, "SP", [])
            self.considerError(lastError, 'Return')
            self._trace(']\n\n    With', (2150, 2161), self.input.position)
            _G_apply_296, lastError = self._apply(self.rule_ReturnBody, "ReturnBody", [])
            self.considerError(lastError, 'Return')
            _locals['rb'] = _G_apply_296
            _G_python_298, lastError = eval(self._G_expr_297, self.globals, _locals), None
            self.considerError(lastError, 'Return')
            return (_G_python_298, self.currentError)


        def rule_ReturnBody(self):
            _locals = {'self': self}
            self.locals['ReturnBody'] = _locals
            self._trace('ReturnBody:r', (2199, 2211), self.input.position)
            _G_apply_299, lastError = self._apply(self.rule_ReturnItems, "ReturnItems", [])
            self.considerError(lastError, 'ReturnBody')
            _locals['ri'] = _G_apply_299
            def _G_optional_300():
                self._trace('er', (2216, 2218), self.input.position)
                _G_apply_301, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('e)?:w ', (2218, 2224), self.input.position)
                _G_apply_302, lastError = self._apply(self.rule_Order, "Order", [])
                self.considerError(lastError, None)
                return (_G_apply_302, self.currentError)
            def _G_optional_303():
                return (None, self.input.nullError())
            _G_or_304, lastError = self._or([_G_optional_300, _G_optional_303])
            self.considerError(lastError, 'ReturnBody')
            _locals['o'] = _G_or_304
            def _G_optional_305():
                self._trace('it', (2230, 2232), self.input.position)
                _G_apply_306, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('h", d', (2232, 2237), self.input.position)
                _G_apply_307, lastError = self._apply(self.rule_Skip, "Skip", [])
                self.considerError(lastError, None)
                return (_G_apply_307, self.currentError)
            def _G_optional_308():
                return (None, self.input.nullError())
            _G_or_309, lastError = self._or([_G_optional_305, _G_optional_308])
            self.considerError(lastError, 'ReturnBody')
            _locals['s'] = _G_or_309
            def _G_optional_310():
                self._trace('w]', (2243, 2245), self.input.position)
                _G_apply_311, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('\n\n    ', (2245, 2251), self.input.position)
                _G_apply_312, lastError = self._apply(self.rule_Limit, "Limit", [])
                self.considerError(lastError, None)
                return (_G_apply_312, self.currentError)
            def _G_optional_313():
                return (None, self.input.nullError())
            _G_or_314, lastError = self._or([_G_optional_310, _G_optional_313])
            self.considerError(lastError, 'ReturnBody')
            _locals['l'] = _G_or_314
            _G_python_316, lastError = eval(self._G_expr_315, self.globals, _locals), None
            self.considerError(lastError, 'ReturnBody')
            return (_G_python_316, self.currentError)


        def rule_ReturnItems(self):
            _locals = {'self': self}
            self.locals['ReturnItems'] = _locals
            def _G_or_317():
                self._trace('rnB', (2303, 2306), self.input.position)
                _G_exactly_318, lastError = self.exactly('*')
                self.considerError(lastError, None)
                return (_G_exactly_318, self.currentError)
            def _G_or_319():
                self._trace('y:rb -> ["R', (2308, 2319), self.input.position)
                _G_apply_320, lastError = self._apply(self.rule_ReturnItem, "ReturnItem", [])
                self.considerError(lastError, None)
                return (_G_apply_320, self.currentError)
            _G_or_321, lastError = self._or([_G_or_317, _G_or_319])
            self.considerError(lastError, 'ReturnItems')
            _locals['head'] = _G_or_321
            def _G_many_322():
                self._trace('Re', (2339, 2341), self.input.position)
                _G_apply_323, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('turn', (2341, 2345), self.input.position)
                _G_exactly_324, lastError = self.exactly(',')
                self.considerError(lastError, None)
                self._trace('Bod', (2345, 2348), self.input.position)
                _G_apply_325, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('y = ReturnI', (2348, 2359), self.input.position)
                _G_apply_326, lastError = self._apply(self.rule_ReturnItem, "ReturnItem", [])
                self.considerError(lastError, None)
                return (_G_apply_326, self.currentError)
            _G_many_327, lastError = self.many(_G_many_322)
            self.considerError(lastError, 'ReturnItems')
            _locals['tail'] = _G_many_327
            _G_python_329, lastError = eval(self._G_expr_328, self.globals, _locals), None
            self.considerError(lastError, 'ReturnItems')
            return (_G_python_329, self.currentError)


        def rule_ReturnItem(self):
            _locals = {'self': self}
            self.locals['ReturnItem'] = _locals
            def _G_or_330():
                self._trace('turnBody", ', (2415, 2426), self.input.position)
                _G_apply_331, lastError = self._apply(self.rule_Expression, "Expression", [])
                self.considerError(lastError, None)
                _locals['ex'] = _G_apply_331
                self._trace(' o,', (2429, 2432), self.input.position)
                _G_apply_332, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace(' s', (2432, 2434), self.input.position)
                _G_apply_333, lastError = self._apply(self.rule_A, "A", [])
                self.considerError(lastError, None)
                self._trace(', ', (2434, 2436), self.input.position)
                _G_apply_334, lastError = self._apply(self.rule_S, "S", [])
                self.considerError(lastError, None)
                self._trace('l]\n', (2436, 2439), self.input.position)
                _G_apply_335, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('\n    ReturnIt', (2439, 2452), self.input.position)
                _G_apply_336, lastError = self._apply(self.rule_SymbolicName, "SymbolicName", [])
                self.considerError(lastError, None)
                _locals['s'] = _G_apply_336
                _G_python_338, lastError = eval(self._G_expr_337, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_338, self.currentError)
            def _G_or_339():
                self._trace("      (WS '", (2492, 2503), self.input.position)
                _G_apply_340, lastError = self._apply(self.rule_Expression, "Expression", [])
                self.considerError(lastError, None)
                _locals['ex'] = _G_apply_340
                _G_python_342, lastError = eval(self._G_expr_341, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_342, self.currentError)
            _G_or_343, lastError = self._or([_G_or_330, _G_or_339])
            self.considerError(lastError, 'ReturnItem')
            return (_G_or_343, self.currentError)


        def rule_Order(self):
            _locals = {'self': self}
            self.locals['Order'] = _locals
            self._trace('s",', (2543, 2546), self.input.position)
            _G_apply_344, lastError = self._apply(self.rule_O, "O", [])
            self.considerError(lastError, 'Order')
            self._trace(' [', (2546, 2548), self.input.position)
            _G_apply_345, lastError = self._apply(self.rule_R, "R", [])
            self.considerError(lastError, 'Order')
            self._trace('he', (2548, 2550), self.input.position)
            _G_apply_346, lastError = self._apply(self.rule_D, "D", [])
            self.considerError(lastError, 'Order')
            self._trace('ad', (2550, 2552), self.input.position)
            _G_apply_347, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'Order')
            self._trace('] ', (2552, 2554), self.input.position)
            _G_apply_348, lastError = self._apply(self.rule_R, "R", [])
            self.considerError(lastError, 'Order')
            self._trace('+ t', (2554, 2557), self.input.position)
            _G_apply_349, lastError = self._apply(self.rule_SP, "SP", [])
            self.considerError(lastError, 'Order')
            self._trace('ai', (2557, 2559), self.input.position)
            _G_apply_350, lastError = self._apply(self.rule_B, "B", [])
            self.considerError(lastError, 'Order')
            self._trace('l]', (2559, 2561), self.input.position)
            _G_apply_351, lastError = self._apply(self.rule_Y, "Y", [])
            self.considerError(lastError, 'Order')
            self._trace('\n\n ', (2561, 2564), self.input.position)
            _G_apply_352, lastError = self._apply(self.rule_SP, "SP", [])
            self.considerError(lastError, 'Order')
            self._trace('   Return', (2564, 2573), self.input.position)
            _G_apply_353, lastError = self._apply(self.rule_SortItem, "SortItem", [])
            self.considerError(lastError, 'Order')
            _locals['head'] = _G_apply_353
            def _G_many_354():
                self._trace('Ex', (2580, 2582), self.input.position)
                _G_apply_355, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('pres', (2582, 2586), self.input.position)
                _G_exactly_356, lastError = self.exactly(',')
                self.considerError(lastError, None)
                self._trace('sio', (2586, 2589), self.input.position)
                _G_apply_357, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('n:ex SP A', (2589, 2598), self.input.position)
                _G_apply_358, lastError = self._apply(self.rule_SortItem, "SortItem", [])
                self.considerError(lastError, None)
                return (_G_apply_358, self.currentError)
            _G_many_359, lastError = self.many(_G_many_354)
            self.considerError(lastError, 'Order')
            _locals['tail'] = _G_many_359
            _G_python_361, lastError = eval(self._G_expr_360, self.globals, _locals), None
            self.considerError(lastError, 'Order')
            return (_G_python_361, self.currentError)


        def rule_Skip(self):
            _locals = {'self': self}
            self.locals['Skip'] = _locals
            self._trace('s]\n', (2641, 2644), self.input.position)
            _G_apply_362, lastError = self._apply(self.rule_S, "S", [])
            self.considerError(lastError, 'Skip')
            self._trace('  ', (2644, 2646), self.input.position)
            _G_apply_363, lastError = self._apply(self.rule_K, "K", [])
            self.considerError(lastError, 'Skip')
            self._trace('  ', (2646, 2648), self.input.position)
            _G_apply_364, lastError = self._apply(self.rule_I, "I", [])
            self.considerError(lastError, 'Skip')
            self._trace('  ', (2648, 2650), self.input.position)
            _G_apply_365, lastError = self._apply(self.rule_P, "P", [])
            self.considerError(lastError, 'Skip')
            self._trace('   ', (2650, 2653), self.input.position)
            _G_apply_366, lastError = self._apply(self.rule_SP, "SP", [])
            self.considerError(lastError, 'Skip')
            self._trace('      | Exp', (2653, 2664), self.input.position)
            _G_apply_367, lastError = self._apply(self.rule_Expression, "Expression", [])
            self.considerError(lastError, 'Skip')
            _locals['ex'] = _G_apply_367
            _G_python_369, lastError = eval(self._G_expr_368, self.globals, _locals), None
            self.considerError(lastError, 'Skip')
            return (_G_python_369, self.currentError)


        def rule_Limit(self):
            _locals = {'self': self}
            self.locals['Limit'] = _locals
            self._trace(' ex', (2692, 2695), self.input.position)
            _G_apply_370, lastError = self._apply(self.rule_L, "L", [])
            self.considerError(lastError, 'Limit')
            self._trace(', ', (2695, 2697), self.input.position)
            _G_apply_371, lastError = self._apply(self.rule_I, "I", [])
            self.considerError(lastError, 'Limit')
            self._trace('No', (2697, 2699), self.input.position)
            _G_apply_372, lastError = self._apply(self.rule_M, "M", [])
            self.considerError(lastError, 'Limit')
            self._trace('ne', (2699, 2701), self.input.position)
            _G_apply_373, lastError = self._apply(self.rule_I, "I", [])
            self.considerError(lastError, 'Limit')
            self._trace(']\n', (2701, 2703), self.input.position)
            _G_apply_374, lastError = self._apply(self.rule_T, "T", [])
            self.considerError(lastError, 'Limit')
            self._trace('\n  ', (2703, 2706), self.input.position)
            _G_apply_375, lastError = self._apply(self.rule_SP, "SP", [])
            self.considerError(lastError, 'Limit')
            self._trace('  Order =  ', (2706, 2717), self.input.position)
            _G_apply_376, lastError = self._apply(self.rule_Expression, "Expression", [])
            self.considerError(lastError, 'Limit')
            _locals['ex'] = _G_apply_376
            _G_python_378, lastError = eval(self._G_expr_377, self.globals, _locals), None
            self.considerError(lastError, 'Limit')
            return (_G_python_378, self.currentError)


        def rule_SortItem(self):
            _locals = {'self': self}
            self.locals['SortItem'] = _locals
            def _G_or_379():
                self._trace("d (WS ',' W", (2749, 2760), self.input.position)
                _G_apply_380, lastError = self._apply(self.rule_Expression, "Expression", [])
                self.considerError(lastError, None)
                _locals['ex'] = _G_apply_380
                def _G_or_381():
                    self._trace('tI', (2765, 2767), self.input.position)
                    _G_apply_382, lastError = self._apply(self.rule_SP, "SP", [])
                    self.considerError(lastError, None)
                    self._trace('te', (2767, 2769), self.input.position)
                    _G_apply_383, lastError = self._apply(self.rule_D, "D", [])
                    self.considerError(lastError, None)
                    self._trace('m)', (2769, 2771), self.input.position)
                    _G_apply_384, lastError = self._apply(self.rule_E, "E", [])
                    self.considerError(lastError, None)
                    self._trace('*:', (2771, 2773), self.input.position)
                    _G_apply_385, lastError = self._apply(self.rule_S, "S", [])
                    self.considerError(lastError, None)
                    self._trace('ta', (2773, 2775), self.input.position)
                    _G_apply_386, lastError = self._apply(self.rule_C, "C", [])
                    self.considerError(lastError, None)
                    self._trace('il', (2775, 2777), self.input.position)
                    _G_apply_387, lastError = self._apply(self.rule_E, "E", [])
                    self.considerError(lastError, None)
                    self._trace(' -', (2777, 2779), self.input.position)
                    _G_apply_388, lastError = self._apply(self.rule_N, "N", [])
                    self.considerError(lastError, None)
                    self._trace('> ', (2779, 2781), self.input.position)
                    _G_apply_389, lastError = self._apply(self.rule_D, "D", [])
                    self.considerError(lastError, None)
                    self._trace('["', (2781, 2783), self.input.position)
                    _G_apply_390, lastError = self._apply(self.rule_I, "I", [])
                    self.considerError(lastError, None)
                    self._trace('Or', (2783, 2785), self.input.position)
                    _G_apply_391, lastError = self._apply(self.rule_N, "N", [])
                    self.considerError(lastError, None)
                    self._trace('de', (2785, 2787), self.input.position)
                    _G_apply_392, lastError = self._apply(self.rule_G, "G", [])
                    self.considerError(lastError, None)
                    return (_G_apply_392, self.currentError)
                def _G_or_393():
                    self._trace(', [', (2789, 2792), self.input.position)
                    _G_apply_394, lastError = self._apply(self.rule_SP, "SP", [])
                    self.considerError(lastError, None)
                    self._trace('he', (2792, 2794), self.input.position)
                    _G_apply_395, lastError = self._apply(self.rule_D, "D", [])
                    self.considerError(lastError, None)
                    self._trace('ad', (2794, 2796), self.input.position)
                    _G_apply_396, lastError = self._apply(self.rule_E, "E", [])
                    self.considerError(lastError, None)
                    self._trace('] ', (2796, 2798), self.input.position)
                    _G_apply_397, lastError = self._apply(self.rule_S, "S", [])
                    self.considerError(lastError, None)
                    self._trace('+ ', (2798, 2800), self.input.position)
                    _G_apply_398, lastError = self._apply(self.rule_C, "C", [])
                    self.considerError(lastError, None)
                    return (_G_apply_398, self.currentError)
                _G_or_399, lastError = self._or([_G_or_381, _G_or_393])
                self.considerError(lastError, None)
                _G_python_401, lastError = eval(self._G_expr_400, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_401, self.currentError)
            def _G_or_402():
                self._trace('sion:ex -> ', (2836, 2847), self.input.position)
                _G_apply_403, lastError = self._apply(self.rule_Expression, "Expression", [])
                self.considerError(lastError, None)
                _locals['ex'] = _G_apply_403
                def _G_optional_404():
                    def _G_or_405():
                        self._trace('p"', (2852, 2854), self.input.position)
                        _G_apply_406, lastError = self._apply(self.rule_SP, "SP", [])
                        self.considerError(lastError, None)
                        self._trace(', ', (2854, 2856), self.input.position)
                        _G_apply_407, lastError = self._apply(self.rule_A, "A", [])
                        self.considerError(lastError, None)
                        self._trace('ex', (2856, 2858), self.input.position)
                        _G_apply_408, lastError = self._apply(self.rule_S, "S", [])
                        self.considerError(lastError, None)
                        self._trace(']\n', (2858, 2860), self.input.position)
                        _G_apply_409, lastError = self._apply(self.rule_C, "C", [])
                        self.considerError(lastError, None)
                        self._trace('\n ', (2860, 2862), self.input.position)
                        _G_apply_410, lastError = self._apply(self.rule_E, "E", [])
                        self.considerError(lastError, None)
                        self._trace('  ', (2862, 2864), self.input.position)
                        _G_apply_411, lastError = self._apply(self.rule_N, "N", [])
                        self.considerError(lastError, None)
                        self._trace(' L', (2864, 2866), self.input.position)
                        _G_apply_412, lastError = self._apply(self.rule_D, "D", [])
                        self.considerError(lastError, None)
                        self._trace('im', (2866, 2868), self.input.position)
                        _G_apply_413, lastError = self._apply(self.rule_I, "I", [])
                        self.considerError(lastError, None)
                        self._trace('it', (2868, 2870), self.input.position)
                        _G_apply_414, lastError = self._apply(self.rule_N, "N", [])
                        self.considerError(lastError, None)
                        self._trace(' =', (2870, 2872), self.input.position)
                        _G_apply_415, lastError = self._apply(self.rule_G, "G", [])
                        self.considerError(lastError, None)
                        return (_G_apply_415, self.currentError)
                    def _G_or_416():
                        self._trace('L I', (2874, 2877), self.input.position)
                        _G_apply_417, lastError = self._apply(self.rule_SP, "SP", [])
                        self.considerError(lastError, None)
                        self._trace(' M', (2877, 2879), self.input.position)
                        _G_apply_418, lastError = self._apply(self.rule_A, "A", [])
                        self.considerError(lastError, None)
                        self._trace(' I', (2879, 2881), self.input.position)
                        _G_apply_419, lastError = self._apply(self.rule_S, "S", [])
                        self.considerError(lastError, None)
                        self._trace(' T', (2881, 2883), self.input.position)
                        _G_apply_420, lastError = self._apply(self.rule_C, "C", [])
                        self.considerError(lastError, None)
                        return (_G_apply_420, self.currentError)
                    _G_or_421, lastError = self._or([_G_or_405, _G_or_416])
                    self.considerError(lastError, None)
                    return (_G_or_421, self.currentError)
                def _G_optional_422():
                    return (None, self.input.nullError())
                _G_or_423, lastError = self._or([_G_optional_404, _G_optional_422])
                self.considerError(lastError, None)
                _G_python_425, lastError = eval(self._G_expr_424, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_425, self.currentError)
            _G_or_426, lastError = self._or([_G_or_379, _G_or_402])
            self.considerError(lastError, 'SortItem')
            return (_G_or_426, self.currentError)


        def rule_Where(self):
            _locals = {'self': self}
            self.locals['Where'] = _locals
            self._trace('\n\n', (2917, 2919), self.input.position)
            _G_apply_427, lastError = self._apply(self.rule_W, "W", [])
            self.considerError(lastError, 'Where')
            self._trace('  ', (2919, 2921), self.input.position)
            _G_apply_428, lastError = self._apply(self.rule_H, "H", [])
            self.considerError(lastError, 'Where')
            self._trace('  ', (2921, 2923), self.input.position)
            _G_apply_429, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'Where')
            self._trace('So', (2923, 2925), self.input.position)
            _G_apply_430, lastError = self._apply(self.rule_R, "R", [])
            self.considerError(lastError, 'Where')
            self._trace('rt', (2925, 2927), self.input.position)
            _G_apply_431, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'Where')
            self._trace('Ite', (2927, 2930), self.input.position)
            _G_apply_432, lastError = self._apply(self.rule_SP, "SP", [])
            self.considerError(lastError, 'Where')
            self._trace('m = Express', (2930, 2941), self.input.position)
            _G_apply_433, lastError = self._apply(self.rule_Expression, "Expression", [])
            self.considerError(lastError, 'Where')
            _locals['ex'] = _G_apply_433
            _G_python_435, lastError = eval(self._G_expr_434, self.globals, _locals), None
            self.considerError(lastError, 'Where')
            return (_G_python_435, self.currentError)


        def rule_Pattern(self):
            _locals = {'self': self}
            self.locals['Pattern'] = _locals
            self._trace('| SP D E S C', (2972, 2984), self.input.position)
            _G_apply_436, lastError = self._apply(self.rule_PatternPart, "PatternPart", [])
            self.considerError(lastError, 'Pattern')
            _locals['head'] = _G_apply_436
            def _G_many_437():
                self._trace('sor', (2991, 2994), self.input.position)
                _G_exactly_438, lastError = self.exactly(',')
                self.considerError(lastError, None)
                self._trace('t",', (2994, 2997), self.input.position)
                _G_apply_439, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace(' ex, "desc"]', (2997, 3009), self.input.position)
                _G_apply_440, lastError = self._apply(self.rule_PatternPart, "PatternPart", [])
                self.considerError(lastError, None)
                return (_G_apply_440, self.currentError)
            _G_many_441, lastError = self.many(_G_many_437)
            self.considerError(lastError, 'Pattern')
            _locals['tail'] = _G_many_441
            _G_python_443, lastError = eval(self._G_expr_442, self.globals, _locals), None
            self.considerError(lastError, 'Pattern')
            return (_G_python_443, self.currentError)


        def rule_PatternPart(self):
            _locals = {'self': self}
            self.locals['PatternPart'] = _locals
            def _G_or_444():
                self._trace(' N D I N', (3050, 3058), self.input.position)
                _G_apply_445, lastError = self._apply(self.rule_Variable, "Variable", [])
                self.considerError(lastError, None)
                _locals['v'] = _G_apply_445
                self._trace(' | ', (3060, 3063), self.input.position)
                _G_apply_446, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('SP A', (3063, 3067), self.input.position)
                _G_exactly_447, lastError = self.exactly('=')
                self.considerError(lastError, None)
                self._trace(' S ', (3067, 3070), self.input.position)
                _G_apply_448, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('C)? -> ["sort", ex, "', (3070, 3091), self.input.position)
                _G_apply_449, lastError = self._apply(self.rule_AnonymousPatternPart, "AnonymousPatternPart", [])
                self.considerError(lastError, None)
                _locals['ap'] = _G_apply_449
                _G_python_451, lastError = eval(self._G_expr_450, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_451, self.currentError)
            def _G_or_452():
                self._trace('-> ["Whe', (3137, 3145), self.input.position)
                _G_apply_453, lastError = self._apply(self.rule_Variable, "Variable", [])
                self.considerError(lastError, None)
                _locals['v'] = _G_apply_453
                self._trace('", e', (3147, 3151), self.input.position)
                _G_exactly_454, lastError = self.exactly(':')
                self.considerError(lastError, None)
                self._trace('x]\n', (3151, 3154), self.input.position)
                _G_apply_455, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('\n    Pattern = Patter', (3154, 3175), self.input.position)
                _G_apply_456, lastError = self._apply(self.rule_AnonymousPatternPart, "AnonymousPatternPart", [])
                self.considerError(lastError, None)
                _locals['ap'] = _G_apply_456
                _G_python_458, lastError = eval(self._G_expr_457, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_458, self.currentError)
            def _G_or_459():
                self._trace(' tail\n\n    PatternPar', (3224, 3245), self.input.position)
                _G_apply_460, lastError = self._apply(self.rule_AnonymousPatternPart, "AnonymousPatternPart", [])
                self.considerError(lastError, None)
                _locals['ap'] = _G_apply_460
                _G_python_462, lastError = eval(self._G_expr_461, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_462, self.currentError)
            _G_or_463, lastError = self._or([_G_or_444, _G_or_452, _G_or_459])
            self.considerError(lastError, 'PatternPart')
            return (_G_or_463, self.currentError)


        def rule_AnonymousPatternPart(self):
            _locals = {'self': self}
            self.locals['AnonymousPatternPart'] = _locals
            self._trace('PatternPart", v', (3301, 3316), self.input.position)
            _G_apply_464, lastError = self._apply(self.rule_PatternElement, "PatternElement", [])
            self.considerError(lastError, 'AnonymousPatternPart')
            return (_G_apply_464, self.currentError)


        def rule_PatternElement(self):
            _locals = {'self': self}
            self.locals['PatternElement'] = _locals
            def _G_or_465():
                self._trace("  | (Variable:v ':' WS Anonymous", (3336, 3368), self.input.position)
                _G_apply_466, lastError = self._apply(self.rule_NodePattern, "NodePattern", [])
                self.considerError(lastError, None)
                _locals['np'] = _G_apply_466
                def _G_many_467():
                    self._trace('hP', (3393, 3395), self.input.position)
                    _G_apply_468, lastError = self._apply(self.rule_WS, "WS", [])
                    self.considerError(lastError, None)
                    self._trace('atternPart", v, ap]\n', (3395, 3415), self.input.position)
                    _G_apply_469, lastError = self._apply(self.rule_PatternElementChain, "PatternElementChain", [])
                    self.considerError(lastError, None)
                    return (_G_apply_469, self.currentError)
                _G_many_470, lastError = self.many(_G_many_467)
                self.considerError(lastError, None)
                _locals['pec'] = _G_many_470
                _G_python_472, lastError = eval(self._G_expr_471, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_472, self.currentError)
            def _G_or_473():
                self._trace('   A', (3488, 3492), self.input.position)
                _G_exactly_474, lastError = self.exactly('(')
                self.considerError(lastError, None)
                self._trace('nonymousPattern', (3492, 3507), self.input.position)
                _G_apply_475, lastError = self._apply(self.rule_PatternElement, "PatternElement", [])
                self.considerError(lastError, None)
                _locals['pe'] = _G_apply_475
                self._trace('t = ', (3510, 3514), self.input.position)
                _G_exactly_476, lastError = self.exactly(')')
                self.considerError(lastError, None)
                _G_python_478, lastError = eval(self._G_expr_477, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_478, self.currentError)
            _G_or_479, lastError = self._or([_G_or_465, _G_or_473])
            self.considerError(lastError, 'PatternElement')
            return (_G_or_479, self.currentError)


        def rule_NodePattern(self):
            _locals = {'self': self}
            self.locals['NodePattern'] = _locals
            self._trace('atte', (3535, 3539), self.input.position)
            _G_exactly_480, lastError = self.exactly('(')
            self.considerError(lastError, 'NodePattern')
            self._trace('rnE', (3539, 3542), self.input.position)
            _G_apply_481, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'NodePattern')
            def _G_optional_482():
                self._trace('                    NodePatte', (3557, 3586), self.input.position)
                _G_apply_483, lastError = self._apply(self.rule_SymbolicName, "SymbolicName", [])
                self.considerError(lastError, None)
                _locals['s'] = _G_apply_483
                self._trace(':np', (3588, 3591), self.input.position)
                _G_apply_484, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                _G_python_485, lastError = eval(self._G_expr_9, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_485, self.currentError)
            def _G_optional_486():
                return (None, self.input.nullError())
            _G_or_487, lastError = self._or([_G_optional_482, _G_optional_486])
            self.considerError(lastError, 'NodePattern')
            _locals['s'] = _G_or_487
            def _G_optional_488():
                self._trace('ementChain)*:pec\n           ', (3629, 3657), self.input.position)
                _G_apply_489, lastError = self._apply(self.rule_NodeLabels, "NodeLabels", [])
                self.considerError(lastError, None)
                _locals['nl'] = _G_apply_489
                self._trace('   ', (3660, 3663), self.input.position)
                _G_apply_490, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                _G_python_492, lastError = eval(self._G_expr_491, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_492, self.currentError)
            def _G_optional_493():
                return (None, self.input.nullError())
            _G_or_494, lastError = self._or([_G_optional_488, _G_optional_493])
            self.considerError(lastError, 'NodePattern')
            _locals['nl'] = _G_or_494
            def _G_optional_495():
                self._trace("                | '(' Patter", (3703, 3731), self.input.position)
                _G_apply_496, lastError = self._apply(self.rule_Properties, "Properties", [])
                self.considerError(lastError, None)
                _locals['p'] = _G_apply_496
                self._trace('lem', (3733, 3736), self.input.position)
                _G_apply_497, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                _G_python_499, lastError = eval(self._G_expr_498, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_499, self.currentError)
            def _G_optional_500():
                return (None, self.input.nullError())
            _G_or_501, lastError = self._or([_G_optional_495, _G_optional_500])
            self.considerError(lastError, 'NodePattern')
            _locals['p'] = _G_or_501
            self._trace("odePattern = '('", (3759, 3775), self.input.position)
            _G_exactly_502, lastError = self.exactly(')')
            self.considerError(lastError, 'NodePattern')
            _G_python_504, lastError = eval(self._G_expr_503, self.globals, _locals), None
            self.considerError(lastError, 'NodePattern')
            return (_G_python_504, self.currentError)


        def rule_PatternElementChain(self):
            _locals = {'self': self}
            self.locals['PatternElementChain'] = _locals
            self._trace('ame:s WS -> s\n      ', (3827, 3847), self.input.position)
            _G_apply_505, lastError = self._apply(self.rule_RelationshipPattern, "RelationshipPattern", [])
            self.considerError(lastError, 'PatternElementChain')
            _locals['rp'] = _G_apply_505
            self._trace('   ', (3850, 3853), self.input.position)
            _G_apply_506, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'PatternElementChain')
            self._trace('     )?:s\n  ', (3853, 3865), self.input.position)
            _G_apply_507, lastError = self._apply(self.rule_NodePattern, "NodePattern", [])
            self.considerError(lastError, 'PatternElementChain')
            _locals['np'] = _G_apply_507
            _G_python_509, lastError = eval(self._G_expr_508, self.globals, _locals), None
            self.considerError(lastError, 'PatternElementChain')
            return (_G_python_509, self.currentError)


        def rule_RelationshipPattern(self):
            _locals = {'self': self}
            self.locals['RelationshipPattern'] = _locals
            def _G_optional_510():
                self._trace('              ', (3926, 3940), self.input.position)
                _G_apply_511, lastError = self._apply(self.rule_LeftArrowHead, "LeftArrowHead", [])
                self.considerError(lastError, None)
                return (_G_apply_511, self.currentError)
            def _G_optional_512():
                return (None, self.input.nullError())
            _G_or_513, lastError = self._or([_G_optional_510, _G_optional_512])
            self.considerError(lastError, 'RelationshipPattern')
            _locals['la'] = _G_or_513
            self._trace('?:n', (3944, 3947), self.input.position)
            _G_apply_514, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'RelationshipPattern')
            self._trace('l\n   ', (3947, 3952), self.input.position)
            _G_apply_515, lastError = self._apply(self.rule_Dash, "Dash", [])
            self.considerError(lastError, 'RelationshipPattern')
            self._trace('   ', (3952, 3955), self.input.position)
            _G_apply_516, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'RelationshipPattern')
            def _G_optional_517():
                self._trace('           (\n      ', (3955, 3974), self.input.position)
                _G_apply_518, lastError = self._apply(self.rule_RelationshipDetail, "RelationshipDetail", [])
                self.considerError(lastError, None)
                return (_G_apply_518, self.currentError)
            def _G_optional_519():
                return (None, self.input.nullError())
            _G_or_520, lastError = self._or([_G_optional_517, _G_optional_519])
            self.considerError(lastError, 'RelationshipPattern')
            _locals['rd'] = _G_or_520
            self._trace('   ', (3978, 3981), self.input.position)
            _G_apply_521, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'RelationshipPattern')
            self._trace('     ', (3981, 3986), self.input.position)
            _G_apply_522, lastError = self._apply(self.rule_Dash, "Dash", [])
            self.considerError(lastError, 'RelationshipPattern')
            self._trace('   ', (3986, 3989), self.input.position)
            _G_apply_523, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'RelationshipPattern')
            def _G_optional_524():
                self._trace('Properties:p WS', (3989, 4004), self.input.position)
                _G_apply_525, lastError = self._apply(self.rule_RightArrowHead, "RightArrowHead", [])
                self.considerError(lastError, None)
                return (_G_apply_525, self.currentError)
            def _G_optional_526():
                return (None, self.input.nullError())
            _G_or_527, lastError = self._or([_G_optional_524, _G_optional_526])
            self.considerError(lastError, 'RelationshipPattern')
            _locals['ra'] = _G_or_527
            _G_python_529, lastError = eval(self._G_expr_528, self.globals, _locals), None
            self.considerError(lastError, 'RelationshipPattern')
            return (_G_python_529, self.currentError)


        def rule_RelationshipDetail(self):
            _locals = {'self': self}
            self.locals['RelationshipDetail'] = _locals
            self._trace('tern', (4157, 4161), self.input.position)
            _G_exactly_530, lastError = self.exactly('[')
            self.considerError(lastError, 'RelationshipDetail')
            def _G_optional_531():
                self._trace('ElementChain", rp, np]\n\n   ', (4161, 4188), self.input.position)
                _G_apply_532, lastError = self._apply(self.rule_Variable, "Variable", [])
                self.considerError(lastError, None)
                return (_G_apply_532, self.currentError)
            def _G_optional_533():
                return (None, self.input.nullError())
            _G_or_534, lastError = self._or([_G_optional_531, _G_optional_533])
            self.considerError(lastError, 'RelationshipDetail')
            _locals['v'] = _G_or_534
            def _G_optional_535():
                self._trace('lationshipPattern = Le', (4191, 4213), self.input.position)
                _G_exactly_536, lastError = self.exactly('?')
                self.considerError(lastError, None)
                return (_G_exactly_536, self.currentError)
            def _G_optional_537():
                return (None, self.input.nullError())
            _G_or_538, lastError = self._or([_G_optional_535, _G_optional_537])
            self.considerError(lastError, 'RelationshipDetail')
            _locals['q'] = _G_or_538
            def _G_optional_539():
                self._trace('rrowHead?:la WS Dash WS Relationship', (4216, 4252), self.input.position)
                _G_apply_540, lastError = self._apply(self.rule_RelationshipTypes, "RelationshipTypes", [])
                self.considerError(lastError, None)
                return (_G_apply_540, self.currentError)
            def _G_optional_541():
                return (None, self.input.nullError())
            _G_or_542, lastError = self._or([_G_optional_539, _G_optional_541])
            self.considerError(lastError, 'RelationshipDetail')
            _locals['rt'] = _G_or_542
            def _G_optional_543():
                self._trace('ght', (4276, 4279), self.input.position)
                _G_exactly_544, lastError = self.exactly('*')
                self.considerError(lastError, None)
                self._trace('ArrowHead?:ra', (4279, 4292), self.input.position)
                _G_apply_545, lastError = self._apply(self.rule_RangeLiteral, "RangeLiteral", [])
                self.considerError(lastError, None)
                return (_G_apply_545, self.currentError)
            def _G_optional_546():
                return (None, self.input.nullError())
            _G_or_547, lastError = self._or([_G_optional_543, _G_optional_546])
            self.considerError(lastError, 'RelationshipDetail')
            _locals['rl'] = _G_or_547
            self._trace('"Re', (4297, 4300), self.input.position)
            _G_apply_548, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'RelationshipDetail')
            def _G_optional_549():
                self._trace('lationshipsPattern", la, rd, ', (4300, 4329), self.input.position)
                _G_apply_550, lastError = self._apply(self.rule_Properties, "Properties", [])
                self.considerError(lastError, None)
                return (_G_apply_550, self.currentError)
            def _G_optional_551():
                return (None, self.input.nullError())
            _G_or_552, lastError = self._or([_G_optional_549, _G_optional_551])
            self.considerError(lastError, 'RelationshipDetail')
            _locals['p'] = _G_or_552
            self._trace('\n\n    # TO DO: fix WS ', (4332, 4354), self.input.position)
            _G_exactly_553, lastError = self.exactly(']')
            self.considerError(lastError, 'RelationshipDetail')
            _G_python_555, lastError = eval(self._G_expr_554, self.globals, _locals), None
            self.considerError(lastError, 'RelationshipDetail')
            return (_G_python_555, self.currentError)


        def rule_Properties(self):
            _locals = {'self': self}
            self.locals['Properties'] = _locals
            def _G_or_556():
                self._trace(' NodePatter', (4411, 4422), self.input.position)
                _G_apply_557, lastError = self._apply(self.rule_MapLiteral, "MapLiteral", [])
                self.considerError(lastError, None)
                return (_G_apply_557, self.currentError)
            def _G_or_558():
                self._trace('onshipDeta', (4435, 4445), self.input.position)
                _G_apply_559, lastError = self._apply(self.rule_Parameter, "Parameter", [])
                self.considerError(lastError, None)
                return (_G_apply_559, self.currentError)
            _G_or_560, lastError = self._or([_G_or_556, _G_or_558])
            self.considerError(lastError, 'Properties')
            return (_G_or_560, self.currentError)


        def rule_RelationshipTypes(self):
            _locals = {'self': self}
            self.locals['RelationshipTypes'] = _locals
            self._trace('    ', (4466, 4470), self.input.position)
            _G_exactly_561, lastError = self.exactly(':')
            self.considerError(lastError, 'RelationshipTypes')
            self._trace('      Variab', (4470, 4482), self.input.position)
            _G_apply_562, lastError = self._apply(self.rule_RelTypeName, "RelTypeName", [])
            self.considerError(lastError, 'RelationshipTypes')
            _locals['head'] = _G_apply_562
            def _G_many_563():
                self._trace('  ', (4489, 4491), self.input.position)
                _G_apply_564, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('    ', (4491, 4495), self.input.position)
                _G_exactly_565, lastError = self.exactly('|')
                self.considerError(lastError, None)
                def _G_optional_566():
                    self._trace('    ', (4495, 4499), self.input.position)
                    _G_exactly_567, lastError = self.exactly(':')
                    self.considerError(lastError, None)
                    return (_G_exactly_567, self.currentError)
                def _G_optional_568():
                    return (None, self.input.nullError())
                _G_or_569, lastError = self._or([_G_optional_566, _G_optional_568])
                self.considerError(lastError, None)
                self._trace('   ', (4500, 4503), self.input.position)
                _G_apply_570, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace("       '?'?:", (4503, 4515), self.input.position)
                _G_apply_571, lastError = self._apply(self.rule_RelTypeName, "RelTypeName", [])
                self.considerError(lastError, None)
                return (_G_apply_571, self.currentError)
            _G_many_572, lastError = self.many(_G_many_563)
            self.considerError(lastError, 'RelationshipTypes')
            _locals['tail'] = _G_many_572
            _G_python_574, lastError = eval(self._G_expr_573, self.globals, _locals), None
            self.considerError(lastError, 'RelationshipTypes')
            return (_G_python_574, self.currentError)


        def rule_NodeLabels(self):
            _locals = {'self': self}
            self.locals['NodeLabels'] = _locals
            self._trace('         (', (4574, 4584), self.input.position)
            _G_apply_575, lastError = self._apply(self.rule_NodeLabel, "NodeLabel", [])
            self.considerError(lastError, 'NodeLabels')
            _locals['head'] = _G_apply_575
            def _G_many_576():
                self._trace('ge', (4591, 4593), self.input.position)
                _G_apply_577, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('Literal)?:', (4593, 4603), self.input.position)
                _G_apply_578, lastError = self._apply(self.rule_NodeLabel, "NodeLabel", [])
                self.considerError(lastError, None)
                return (_G_apply_578, self.currentError)
            _G_many_579, lastError = self.many(_G_many_576)
            self.considerError(lastError, 'NodeLabels')
            _locals['tail'] = _G_many_579
            _G_python_580, lastError = eval(self._G_expr_442, self.globals, _locals), None
            self.considerError(lastError, 'NodeLabels')
            return (_G_python_580, self.currentError)


        def rule_NodeLabel(self):
            _locals = {'self': self}
            self.locals['NodeLabel'] = _locals
            self._trace('s?:p', (4640, 4644), self.input.position)
            _G_exactly_581, lastError = self.exactly(':')
            self.considerError(lastError, 'NodeLabel')
            self._trace('\n         ', (4644, 4654), self.input.position)
            _G_apply_582, lastError = self._apply(self.rule_LabelName, "LabelName", [])
            self.considerError(lastError, 'NodeLabel')
            _locals['n'] = _G_apply_582
            _G_python_584, lastError = eval(self._G_expr_583, self.globals, _locals), None
            self.considerError(lastError, 'NodeLabel')
            return (_G_python_584, self.currentError)


        def rule_RangeLiteral(self):
            _locals = {'self': self}
            self.locals['RangeLiteral'] = _locals
            def _G_optional_585():
                self._trace('",', (4694, 4696), self.input.position)
                _G_apply_586, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace(' v, q, rt, rl, ', (4696, 4711), self.input.position)
                _G_apply_587, lastError = self._apply(self.rule_IntegerLiteral, "IntegerLiteral", [])
                self.considerError(lastError, None)
                return (_G_apply_587, self.currentError)
            def _G_optional_588():
                return (None, self.input.nullError())
            _G_or_589, lastError = self._or([_G_optional_585, _G_optional_588])
            self.considerError(lastError, 'RangeLiteral')
            _locals['start'] = _G_or_589
            self._trace('Pro', (4719, 4722), self.input.position)
            _G_apply_590, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'RangeLiteral')
            def _G_optional_591():
                self._trace('rtie', (4724, 4728), self.input.position)
                _G_exactly_592, lastError = self.exactly('..')
                self.considerError(lastError, None)
                self._trace('s =', (4728, 4731), self.input.position)
                _G_apply_593, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace(' MapLiteral\n   ', (4731, 4746), self.input.position)
                _G_apply_594, lastError = self._apply(self.rule_IntegerLiteral, "IntegerLiteral", [])
                self.considerError(lastError, None)
                return (_G_apply_594, self.currentError)
            def _G_optional_595():
                return (None, self.input.nullError())
            _G_or_596, lastError = self._or([_G_optional_591, _G_optional_595])
            self.considerError(lastError, 'RangeLiteral')
            _locals['stop'] = _G_or_596
            self._trace('   ', (4753, 4756), self.input.position)
            _G_apply_597, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'RangeLiteral')
            _G_python_599, lastError = eval(self._G_expr_598, self.globals, _locals), None
            self.considerError(lastError, 'RangeLiteral')
            return (_G_python_599, self.currentError)


        def rule_LabelName(self):
            _locals = {'self': self}
            self.locals['LabelName'] = _locals
            self._trace("s = ':' RelTy", (4791, 4804), self.input.position)
            _G_apply_600, lastError = self._apply(self.rule_SymbolicName, "SymbolicName", [])
            self.considerError(lastError, 'LabelName')
            return (_G_apply_600, self.currentError)


        def rule_RelTypeName(self):
            _locals = {'self': self}
            self.locals['RelTypeName'] = _locals
            self._trace(" '|' ':'? WS ", (4819, 4832), self.input.position)
            _G_apply_601, lastError = self._apply(self.rule_SymbolicName, "SymbolicName", [])
            self.considerError(lastError, 'RelTypeName')
            return (_G_apply_601, self.currentError)


        def rule_Expression(self):
            _locals = {'self': self}
            self.locals['Expression'] = _locals
            self._trace('tail -> ["Rel', (4846, 4859), self.input.position)
            _G_apply_602, lastError = self._apply(self.rule_Expression12, "Expression12", [])
            self.considerError(lastError, 'Expression')
            return (_G_apply_602, self.currentError)


        def rule_Expression12(self):
            _locals = {'self': self}
            self.locals['Expression12'] = _locals
            def _G_or_603():
                self._trace(' head] + tail', (4875, 4888), self.input.position)
                _G_apply_604, lastError = self._apply(self.rule_Expression11, "Expression11", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_604
                self._trace('  N', (4892, 4895), self.input.position)
                _G_apply_605, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('od', (4895, 4897), self.input.position)
                _G_apply_606, lastError = self._apply(self.rule_O, "O", [])
                self.considerError(lastError, None)
                self._trace('eL', (4897, 4899), self.input.position)
                _G_apply_607, lastError = self._apply(self.rule_R, "R", [])
                self.considerError(lastError, None)
                self._trace('abe', (4899, 4902), self.input.position)
                _G_apply_608, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('ls = NodeLabe', (4902, 4915), self.input.position)
                _G_apply_609, lastError = self._apply(self.rule_Expression12, "Expression12", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_609
                _G_python_611, lastError = eval(self._G_expr_610, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_611, self.currentError)
            def _G_or_612():
                self._trace(' tail\n\n    No', (4954, 4967), self.input.position)
                _G_apply_613, lastError = self._apply(self.rule_Expression11, "Expression11", [])
                self.considerError(lastError, None)
                return (_G_apply_613, self.currentError)
            _G_or_614, lastError = self._or([_G_or_603, _G_or_612])
            self.considerError(lastError, 'Expression12')
            return (_G_or_614, self.currentError)


        def rule_Expression11(self):
            _locals = {'self': self}
            self.locals['Expression11'] = _locals
            def _G_or_615():
                self._trace('belName:n -> ', (4983, 4996), self.input.position)
                _G_apply_616, lastError = self._apply(self.rule_Expression10, "Expression10", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_616
                self._trace('deL', (5000, 5003), self.input.position)
                _G_apply_617, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('ab', (5003, 5005), self.input.position)
                _G_apply_618, lastError = self._apply(self.rule_X, "X", [])
                self.considerError(lastError, None)
                self._trace('el', (5005, 5007), self.input.position)
                _G_apply_619, lastError = self._apply(self.rule_O, "O", [])
                self.considerError(lastError, None)
                self._trace('",', (5007, 5009), self.input.position)
                _G_apply_620, lastError = self._apply(self.rule_R, "R", [])
                self.considerError(lastError, None)
                self._trace(' n]', (5009, 5012), self.input.position)
                _G_apply_621, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('\n\n    RangeLi', (5012, 5025), self.input.position)
                _G_apply_622, lastError = self._apply(self.rule_Expression11, "Expression11", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_622
                _G_python_624, lastError = eval(self._G_expr_623, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_624, self.currentError)
            def _G_or_625():
                self._trace("..' WS Intege", (5065, 5078), self.input.position)
                _G_apply_626, lastError = self._apply(self.rule_Expression10, "Expression10", [])
                self.considerError(lastError, None)
                return (_G_apply_626, self.currentError)
            _G_or_627, lastError = self._or([_G_or_615, _G_or_625])
            self.considerError(lastError, 'Expression11')
            return (_G_or_627, self.currentError)


        def rule_Expression10(self):
            _locals = {'self': self}
            self.locals['Expression10'] = _locals
            def _G_or_628():
                self._trace('WS -> slice(', (5094, 5106), self.input.position)
                _G_apply_629, lastError = self._apply(self.rule_Expression9, "Expression9", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_629
                self._trace('t, ', (5110, 5113), self.input.position)
                _G_apply_630, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('st', (5113, 5115), self.input.position)
                _G_apply_631, lastError = self._apply(self.rule_A, "A", [])
                self.considerError(lastError, None)
                self._trace('op', (5115, 5117), self.input.position)
                _G_apply_632, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace(')\n', (5117, 5119), self.input.position)
                _G_apply_633, lastError = self._apply(self.rule_D, "D", [])
                self.considerError(lastError, None)
                self._trace('\n  ', (5119, 5122), self.input.position)
                _G_apply_634, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('  LabelName =', (5122, 5135), self.input.position)
                _G_apply_635, lastError = self._apply(self.rule_Expression10, "Expression10", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_635
                _G_python_637, lastError = eval(self._G_expr_636, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_637, self.currentError)
            def _G_or_638():
                self._trace('cName\n\n    E', (5175, 5187), self.input.position)
                _G_apply_639, lastError = self._apply(self.rule_Expression9, "Expression9", [])
                self.considerError(lastError, None)
                return (_G_apply_639, self.currentError)
            _G_or_640, lastError = self._or([_G_or_628, _G_or_638])
            self.considerError(lastError, 'Expression10')
            return (_G_or_640, self.currentError)


        def rule_Expression9(self):
            _locals = {'self': self}
            self.locals['Expression9'] = _locals
            def _G_or_641():
                self._trace('re', (5202, 5204), self.input.position)
                _G_apply_642, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace('ss', (5204, 5206), self.input.position)
                _G_apply_643, lastError = self._apply(self.rule_O, "O", [])
                self.considerError(lastError, None)
                self._trace('io', (5206, 5208), self.input.position)
                _G_apply_644, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                self._trace('n12', (5208, 5211), self.input.position)
                _G_apply_645, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('\n\n    Expres', (5211, 5223), self.input.position)
                _G_apply_646, lastError = self._apply(self.rule_Expression9, "Expression9", [])
                self.considerError(lastError, None)
                _locals['ex'] = _G_apply_646
                _G_python_648, lastError = eval(self._G_expr_647, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_648, self.currentError)
            def _G_or_649():
                self._trace(' SP Expressi', (5255, 5267), self.input.position)
                _G_apply_650, lastError = self._apply(self.rule_Expression8, "Expression8", [])
                self.considerError(lastError, None)
                return (_G_apply_650, self.currentError)
            _G_or_651, lastError = self._or([_G_or_641, _G_or_649])
            self.considerError(lastError, 'Expression9')
            return (_G_or_651, self.currentError)


        def rule_Expression8(self):
            _locals = {'self': self}
            self.locals['Expression8'] = _locals
            def _G_or_652():
                self._trace('r", ex1, ex2', (5282, 5294), self.input.position)
                _G_apply_653, lastError = self._apply(self.rule_Expression7, "Expression7", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_653
                self._trace('   ', (5298, 5301), self.input.position)
                _G_apply_654, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('    ', (5301, 5305), self.input.position)
                _G_exactly_655, lastError = self.exactly('=')
                self.considerError(lastError, None)
                self._trace('    ', (5305, 5309), self.input.position)
                _G_apply_656, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('    | Expres', (5309, 5321), self.input.position)
                _G_apply_657, lastError = self._apply(self.rule_Expression8, "Expression8", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_657
                _G_python_659, lastError = eval(self._G_expr_658, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_659, self.currentError)
            def _G_or_660():
                self._trace(':ex1 SP X O ', (5360, 5372), self.input.position)
                _G_apply_661, lastError = self._apply(self.rule_Expression7, "Expression7", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_661
                self._trace(' Ex', (5376, 5379), self.input.position)
                _G_apply_662, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('press', (5379, 5384), self.input.position)
                _G_exactly_663, lastError = self.exactly('<>')
                self.considerError(lastError, None)
                self._trace('ion', (5384, 5387), self.input.position)
                _G_apply_664, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('11:ex2 -> ["', (5387, 5399), self.input.position)
                _G_apply_665, lastError = self._apply(self.rule_Expression8, "Expression8", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_665
                _G_python_667, lastError = eval(self._G_expr_666, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_667, self.currentError)
            def _G_or_668():
                self._trace('ession10\n\n  ', (5438, 5450), self.input.position)
                _G_apply_669, lastError = self._apply(self.rule_Expression7, "Expression7", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_669
                self._trace('pre', (5454, 5457), self.input.position)
                _G_apply_670, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('ssion', (5457, 5462), self.input.position)
                _G_exactly_671, lastError = self.exactly('!=')
                self.considerError(lastError, None)
                self._trace('10 ', (5462, 5465), self.input.position)
                _G_apply_672, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('= Expression', (5465, 5477), self.input.position)
                _G_apply_673, lastError = self._apply(self.rule_Expression8, "Expression8", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_673
                _G_python_674, lastError = eval(self._G_expr_666, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_674, self.currentError)
            def _G_or_675():
                self._trace('"and", ex1, ', (5516, 5528), self.input.position)
                _G_apply_676, lastError = self._apply(self.rule_Expression7, "Expression7", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_676
                self._trace('\n  ', (5532, 5535), self.input.position)
                _G_apply_677, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('    ', (5535, 5539), self.input.position)
                _G_exactly_678, lastError = self.exactly('<')
                self.considerError(lastError, None)
                self._trace('    ', (5539, 5543), self.input.position)
                _G_apply_679, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('       | Exp', (5543, 5555), self.input.position)
                _G_apply_680, lastError = self._apply(self.rule_Expression8, "Expression8", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_680
                _G_python_682, lastError = eval(self._G_expr_681, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_682, self.currentError)
            def _G_or_683():
                self._trace('pression9:ex', (5594, 5606), self.input.position)
                _G_apply_684, lastError = self._apply(self.rule_Expression7, "Expression7", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_684
                self._trace('["n', (5610, 5613), self.input.position)
                _G_apply_685, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('ot",', (5613, 5617), self.input.position)
                _G_exactly_686, lastError = self.exactly('>')
                self.considerError(lastError, None)
                self._trace(' ex]', (5617, 5621), self.input.position)
                _G_apply_687, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('\n           ', (5621, 5633), self.input.position)
                _G_apply_688, lastError = self._apply(self.rule_Expression8, "Expression8", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_688
                _G_python_690, lastError = eval(self._G_expr_689, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_690, self.currentError)
            def _G_or_691():
                self._trace('xpression7:e', (5672, 5684), self.input.position)
                _G_apply_692, lastError = self._apply(self.rule_Expression7, "Expression7", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_692
                self._trace("S '", (5688, 5691), self.input.position)
                _G_apply_693, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace("='  W", (5691, 5696), self.input.position)
                _G_exactly_694, lastError = self.exactly('<=')
                self.considerError(lastError, None)
                self._trace('S E', (5696, 5699), self.input.position)
                _G_apply_695, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('xpression8:e', (5699, 5711), self.input.position)
                _G_apply_696, lastError = self._apply(self.rule_Expression8, "Expression8", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_696
                _G_python_698, lastError = eval(self._G_expr_697, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_698, self.currentError)
            def _G_or_699():
                self._trace(' | Expressio', (5750, 5762), self.input.position)
                _G_apply_700, lastError = self._apply(self.rule_Expression7, "Expression7", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_700
                self._trace('x1 ', (5766, 5769), self.input.position)
                _G_apply_701, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace("WS '<", (5769, 5774), self.input.position)
                _G_exactly_702, lastError = self.exactly('>=')
                self.considerError(lastError, None)
                self._trace(">' ", (5774, 5777), self.input.position)
                _G_apply_703, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('WS Expressio', (5777, 5789), self.input.position)
                _G_apply_704, lastError = self._apply(self.rule_Expression8, "Expression8", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_704
                _G_python_706, lastError = eval(self._G_expr_705, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_706, self.currentError)
            def _G_or_707():
                self._trace('     | Expre', (5828, 5840), self.input.position)
                _G_apply_708, lastError = self._apply(self.rule_Expression7, "Expression7", [])
                self.considerError(lastError, None)
                return (_G_apply_708, self.currentError)
            _G_or_709, lastError = self._or([_G_or_652, _G_or_660, _G_or_668, _G_or_675, _G_or_683, _G_or_691, _G_or_699, _G_or_707])
            self.considerError(lastError, 'Expression8')
            return (_G_or_709, self.currentError)


        def rule_Expression7(self):
            _locals = {'self': self}
            self.locals['Expression7'] = _locals
            def _G_or_710():
                self._trace("!=' WS Expre", (5855, 5867), self.input.position)
                _G_apply_711, lastError = self._apply(self.rule_Expression6, "Expression6", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_711
                self._trace('n8:', (5871, 5874), self.input.position)
                _G_apply_712, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('ex2 ', (5874, 5878), self.input.position)
                _G_exactly_713, lastError = self.exactly('+')
                self.considerError(lastError, None)
                self._trace('-> ', (5878, 5881), self.input.position)
                _G_apply_714, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('["neq", ex1,', (5881, 5893), self.input.position)
                _G_apply_715, lastError = self._apply(self.rule_Expression7, "Expression7", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_715
                _G_python_717, lastError = eval(self._G_expr_716, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_717, self.currentError)
            def _G_or_718():
                self._trace(" WS '<'  WS ", (5932, 5944), self.input.position)
                _G_apply_719, lastError = self._apply(self.rule_Expression6, "Expression6", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_719
                self._trace('ess', (5948, 5951), self.input.position)
                _G_apply_720, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('ion8', (5951, 5955), self.input.position)
                _G_exactly_721, lastError = self.exactly('-')
                self.considerError(lastError, None)
                self._trace(':ex', (5955, 5958), self.input.position)
                _G_apply_722, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('2 -> ["lt", ', (5958, 5970), self.input.position)
                _G_apply_723, lastError = self._apply(self.rule_Expression7, "Expression7", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_723
                _G_python_725, lastError = eval(self._G_expr_724, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_725, self.currentError)
            def _G_or_726():
                self._trace("7:ex1 WS '>'", (6009, 6021), self.input.position)
                _G_apply_727, lastError = self._apply(self.rule_Expression6, "Expression6", [])
                self.considerError(lastError, None)
                return (_G_apply_727, self.currentError)
            _G_or_728, lastError = self._or([_G_or_710, _G_or_718, _G_or_726])
            self.considerError(lastError, 'Expression7')
            return (_G_or_728, self.currentError)


        def rule_Expression6(self):
            _locals = {'self': self}
            self.locals['Expression6'] = _locals
            def _G_or_729():
                self._trace('8:ex2 -> ["g', (6036, 6048), self.input.position)
                _G_apply_730, lastError = self._apply(self.rule_Expression5, "Expression5", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_730
                self._trace(' ex', (6052, 6055), self.input.position)
                _G_apply_731, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('1, e', (6055, 6059), self.input.position)
                _G_exactly_732, lastError = self.exactly('*')
                self.considerError(lastError, None)
                self._trace('x2]', (6059, 6062), self.input.position)
                _G_apply_733, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('\n           ', (6062, 6074), self.input.position)
                _G_apply_734, lastError = self._apply(self.rule_Expression6, "Expression6", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_734
                _G_python_736, lastError = eval(self._G_expr_735, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_736, self.currentError)
            def _G_or_737():
                self._trace('ion8:ex2 -> ', (6115, 6127), self.input.position)
                _G_apply_738, lastError = self._apply(self.rule_Expression5, "Expression5", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_738
                self._trace('e",', (6131, 6134), self.input.position)
                _G_apply_739, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace(' ex1', (6134, 6138), self.input.position)
                _G_exactly_740, lastError = self.exactly('/')
                self.considerError(lastError, None)
                self._trace(', e', (6138, 6141), self.input.position)
                _G_apply_741, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('x2]\n        ', (6141, 6153), self.input.position)
                _G_apply_742, lastError = self._apply(self.rule_Expression6, "Expression6", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_742
                _G_python_744, lastError = eval(self._G_expr_743, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_744, self.currentError)
            def _G_or_745():
                self._trace('ession8:ex2 ', (6194, 6206), self.input.position)
                _G_apply_746, lastError = self._apply(self.rule_Expression5, "Expression5", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_746
                self._trace('"gt', (6210, 6213), self.input.position)
                _G_apply_747, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('e", ', (6213, 6217), self.input.position)
                _G_exactly_748, lastError = self.exactly('%')
                self.considerError(lastError, None)
                self._trace('ex1', (6217, 6220), self.input.position)
                _G_apply_749, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace(', ex2]\n     ', (6220, 6232), self.input.position)
                _G_apply_750, lastError = self._apply(self.rule_Expression6, "Expression6", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_750
                _G_python_752, lastError = eval(self._G_expr_751, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_752, self.currentError)
            def _G_or_753():
                self._trace(' = Expressio', (6273, 6285), self.input.position)
                _G_apply_754, lastError = self._apply(self.rule_Expression5, "Expression5", [])
                self.considerError(lastError, None)
                return (_G_apply_754, self.currentError)
            _G_or_755, lastError = self._or([_G_or_729, _G_or_737, _G_or_745, _G_or_753])
            self.considerError(lastError, 'Expression6')
            return (_G_or_755, self.currentError)


        def rule_Expression5(self):
            _locals = {'self': self}
            self.locals['Expression5'] = _locals
            def _G_or_756():
                self._trace('S Expression', (6300, 6312), self.input.position)
                _G_apply_757, lastError = self._apply(self.rule_Expression4, "Expression4", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_757
                self._trace('2 -', (6316, 6319), self.input.position)
                _G_apply_758, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('> ["', (6319, 6323), self.input.position)
                _G_exactly_759, lastError = self.exactly('^')
                self.considerError(lastError, None)
                self._trace('add', (6323, 6326), self.input.position)
                _G_apply_760, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('", ex1, ex2]', (6326, 6338), self.input.position)
                _G_apply_761, lastError = self._apply(self.rule_Expression5, "Expression5", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_761
                _G_python_763, lastError = eval(self._G_expr_762, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_763, self.currentError)
            def _G_or_764():
                self._trace("-' WS Expres", (6377, 6389), self.input.position)
                _G_apply_765, lastError = self._apply(self.rule_Expression4, "Expression4", [])
                self.considerError(lastError, None)
                return (_G_apply_765, self.currentError)
            _G_or_766, lastError = self._or([_G_or_756, _G_or_764])
            self.considerError(lastError, 'Expression5')
            return (_G_or_766, self.currentError)


        def rule_Expression4(self):
            _locals = {'self': self}
            self.locals['Expression4'] = _locals
            def _G_or_767():
                self._trace('sub"', (6404, 6408), self.input.position)
                _G_exactly_768, lastError = self.exactly('+')
                self.considerError(lastError, None)
                self._trace(', e', (6408, 6411), self.input.position)
                _G_apply_769, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('x1, ex2]\n   ', (6411, 6423), self.input.position)
                _G_apply_770, lastError = self._apply(self.rule_Expression4, "Expression4", [])
                self.considerError(lastError, None)
                return (_G_apply_770, self.currentError)
            def _G_or_771():
                self._trace(' Exp', (6437, 6441), self.input.position)
                _G_exactly_772, lastError = self.exactly('-')
                self.considerError(lastError, None)
                self._trace('res', (6441, 6444), self.input.position)
                _G_apply_773, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('sion6\n\n    E', (6444, 6456), self.input.position)
                _G_apply_774, lastError = self._apply(self.rule_Expression4, "Expression4", [])
                self.considerError(lastError, None)
                _locals['ex'] = _G_apply_774
                _G_python_776, lastError = eval(self._G_expr_775, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_776, self.currentError)
            def _G_or_777():
                self._trace("' WS Express", (6490, 6502), self.input.position)
                _G_apply_778, lastError = self._apply(self.rule_Expression3, "Expression3", [])
                self.considerError(lastError, None)
                return (_G_apply_778, self.currentError)
            _G_or_779, lastError = self._or([_G_or_767, _G_or_771, _G_or_777])
            self.considerError(lastError, 'Expression4')
            return (_G_or_779, self.currentError)


        def rule_Expression3(self):
            _locals = {'self': self}
            self.locals['Expression3'] = _locals
            def _G_or_780():
                self._trace('ulti", ex1, ', (6517, 6529), self.input.position)
                _G_apply_781, lastError = self._apply(self.rule_Expression2, "Expression2", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_781
                def _G_many1_782():
                    def _G_or_783():
                        self._trace(' | Expression5:ex1 ', (6549, 6568), self.input.position)
                        _G_apply_784, lastError = self._apply(self.rule_WS, "WS", [])
                        self.considerError(lastError, None)
                        self._trace("WS '", (6568, 6572), self.input.position)
                        _G_exactly_785, lastError = self.exactly('[')
                        self.considerError(lastError, None)
                        self._trace("/' WS Expre", (6572, 6583), self.input.position)
                        _G_apply_786, lastError = self._apply(self.rule_Expression, "Expression", [])
                        self.considerError(lastError, None)
                        _locals['prop_name'] = _G_apply_786
                        self._trace(' -> ', (6593, 6597), self.input.position)
                        _G_exactly_787, lastError = self.exactly(']')
                        self.considerError(lastError, None)
                        _G_python_789, lastError = eval(self._G_expr_788, self.globals, _locals), None
                        self.considerError(lastError, None)
                        return (_G_python_789, self.currentError)
                    def _G_or_790():
                        self._trace('x1 ', (6648, 6651), self.input.position)
                        _G_apply_791, lastError = self._apply(self.rule_WS, "WS", [])
                        self.considerError(lastError, None)
                        self._trace("WS '", (6651, 6655), self.input.position)
                        _G_exactly_792, lastError = self.exactly('[')
                        self.considerError(lastError, None)
                        def _G_optional_793():
                            self._trace("%' WS Expre", (6655, 6666), self.input.position)
                            _G_apply_794, lastError = self._apply(self.rule_Expression, "Expression", [])
                            self.considerError(lastError, None)
                            return (_G_apply_794, self.currentError)
                        def _G_optional_795():
                            return (None, self.input.nullError())
                        _G_or_796, lastError = self._or([_G_optional_793, _G_optional_795])
                        self.considerError(lastError, None)
                        _locals['start'] = _G_or_796
                        self._trace('ex2 -', (6673, 6678), self.input.position)
                        _G_exactly_797, lastError = self.exactly('..')
                        self.considerError(lastError, None)
                        def _G_optional_798():
                            self._trace('> ["mod",  ', (6678, 6689), self.input.position)
                            _G_apply_799, lastError = self._apply(self.rule_Expression, "Expression", [])
                            self.considerError(lastError, None)
                            return (_G_apply_799, self.currentError)
                        def _G_optional_800():
                            return (None, self.input.nullError())
                        _G_or_801, lastError = self._or([_G_optional_798, _G_optional_800])
                        self.considerError(lastError, None)
                        _locals['end'] = _G_or_801
                        self._trace(' ex2', (6694, 6698), self.input.position)
                        _G_exactly_802, lastError = self.exactly(']')
                        self.considerError(lastError, None)
                        _G_python_804, lastError = eval(self._G_expr_803, self.globals, _locals), None
                        self.considerError(lastError, None)
                        return (_G_python_804, self.currentError)
                    def _G_or_805():
                        def _G_or_806():
                            self._trace('on5 = Expression4:ex1 W', (6743, 6766), self.input.position)
                            _G_apply_807, lastError = self._apply(self.rule_WS, "WS", [])
                            self.considerError(lastError, None)
                            self._trace("S '^'", (6766, 6771), self.input.position)
                            _G_exactly_808, lastError = self.exactly('=~')
                            self.considerError(lastError, None)
                            _G_python_809, lastError = ("regex"), None
                            self.considerError(lastError, None)
                            return (_G_python_809, self.currentError)
                        def _G_or_810():
                            self._trace('1, ', (6804, 6807), self.input.position)
                            _G_apply_811, lastError = self._apply(self.rule_SP, "SP", [])
                            self.considerError(lastError, None)
                            self._trace('ex', (6807, 6809), self.input.position)
                            _G_apply_812, lastError = self._apply(self.rule_I, "I", [])
                            self.considerError(lastError, None)
                            self._trace('2]', (6809, 6811), self.input.position)
                            _G_apply_813, lastError = self._apply(self.rule_N, "N", [])
                            self.considerError(lastError, None)
                            _G_python_814, lastError = ("in"), None
                            self.considerError(lastError, None)
                            return (_G_python_814, self.currentError)
                        def _G_or_815():
                            self._trace('\n\n ', (6841, 6844), self.input.position)
                            _G_apply_816, lastError = self._apply(self.rule_SP, "SP", [])
                            self.considerError(lastError, None)
                            self._trace('  ', (6844, 6846), self.input.position)
                            _G_apply_817, lastError = self._apply(self.rule_S, "S", [])
                            self.considerError(lastError, None)
                            self._trace(' E', (6846, 6848), self.input.position)
                            _G_apply_818, lastError = self._apply(self.rule_T, "T", [])
                            self.considerError(lastError, None)
                            self._trace('xp', (6848, 6850), self.input.position)
                            _G_apply_819, lastError = self._apply(self.rule_A, "A", [])
                            self.considerError(lastError, None)
                            self._trace('re', (6850, 6852), self.input.position)
                            _G_apply_820, lastError = self._apply(self.rule_R, "R", [])
                            self.considerError(lastError, None)
                            self._trace('ss', (6852, 6854), self.input.position)
                            _G_apply_821, lastError = self._apply(self.rule_T, "T", [])
                            self.considerError(lastError, None)
                            self._trace('io', (6854, 6856), self.input.position)
                            _G_apply_822, lastError = self._apply(self.rule_S, "S", [])
                            self.considerError(lastError, None)
                            self._trace('n4 ', (6856, 6859), self.input.position)
                            _G_apply_823, lastError = self._apply(self.rule_SP, "SP", [])
                            self.considerError(lastError, None)
                            self._trace('= ', (6859, 6861), self.input.position)
                            _G_apply_824, lastError = self._apply(self.rule_W, "W", [])
                            self.considerError(lastError, None)
                            self._trace("'+", (6861, 6863), self.input.position)
                            _G_apply_825, lastError = self._apply(self.rule_I, "I", [])
                            self.considerError(lastError, None)
                            self._trace("' ", (6863, 6865), self.input.position)
                            _G_apply_826, lastError = self._apply(self.rule_T, "T", [])
                            self.considerError(lastError, None)
                            self._trace('WS', (6865, 6867), self.input.position)
                            _G_apply_827, lastError = self._apply(self.rule_H, "H", [])
                            self.considerError(lastError, None)
                            _G_python_828, lastError = ("starts_with"), None
                            self.considerError(lastError, None)
                            return (_G_python_828, self.currentError)
                        def _G_or_829():
                            self._trace('xpr', (6906, 6909), self.input.position)
                            _G_apply_830, lastError = self._apply(self.rule_SP, "SP", [])
                            self.considerError(lastError, None)
                            self._trace('es', (6909, 6911), self.input.position)
                            _G_apply_831, lastError = self._apply(self.rule_E, "E", [])
                            self.considerError(lastError, None)
                            self._trace('si', (6911, 6913), self.input.position)
                            _G_apply_832, lastError = self._apply(self.rule_N, "N", [])
                            self.considerError(lastError, None)
                            self._trace('on', (6913, 6915), self.input.position)
                            _G_apply_833, lastError = self._apply(self.rule_D, "D", [])
                            self.considerError(lastError, None)
                            self._trace('4:', (6915, 6917), self.input.position)
                            _G_apply_834, lastError = self._apply(self.rule_S, "S", [])
                            self.considerError(lastError, None)
                            self._trace('ex ', (6917, 6920), self.input.position)
                            _G_apply_835, lastError = self._apply(self.rule_SP, "SP", [])
                            self.considerError(lastError, None)
                            self._trace('->', (6920, 6922), self.input.position)
                            _G_apply_836, lastError = self._apply(self.rule_W, "W", [])
                            self.considerError(lastError, None)
                            self._trace(' [', (6922, 6924), self.input.position)
                            _G_apply_837, lastError = self._apply(self.rule_I, "I", [])
                            self.considerError(lastError, None)
                            self._trace('"m', (6924, 6926), self.input.position)
                            _G_apply_838, lastError = self._apply(self.rule_T, "T", [])
                            self.considerError(lastError, None)
                            self._trace('in', (6926, 6928), self.input.position)
                            _G_apply_839, lastError = self._apply(self.rule_H, "H", [])
                            self.considerError(lastError, None)
                            _G_python_840, lastError = ("ends_with"), None
                            self.considerError(lastError, None)
                            return (_G_python_840, self.currentError)
                        def _G_or_841():
                            self._trace('\n\n ', (6966, 6969), self.input.position)
                            _G_apply_842, lastError = self._apply(self.rule_SP, "SP", [])
                            self.considerError(lastError, None)
                            self._trace('  ', (6969, 6971), self.input.position)
                            _G_apply_843, lastError = self._apply(self.rule_C, "C", [])
                            self.considerError(lastError, None)
                            self._trace(' E', (6971, 6973), self.input.position)
                            _G_apply_844, lastError = self._apply(self.rule_O, "O", [])
                            self.considerError(lastError, None)
                            self._trace('xp', (6973, 6975), self.input.position)
                            _G_apply_845, lastError = self._apply(self.rule_N, "N", [])
                            self.considerError(lastError, None)
                            self._trace('re', (6975, 6977), self.input.position)
                            _G_apply_846, lastError = self._apply(self.rule_T, "T", [])
                            self.considerError(lastError, None)
                            self._trace('ss', (6977, 6979), self.input.position)
                            _G_apply_847, lastError = self._apply(self.rule_A, "A", [])
                            self.considerError(lastError, None)
                            self._trace('io', (6979, 6981), self.input.position)
                            _G_apply_848, lastError = self._apply(self.rule_I, "I", [])
                            self.considerError(lastError, None)
                            self._trace('n3', (6981, 6983), self.input.position)
                            _G_apply_849, lastError = self._apply(self.rule_N, "N", [])
                            self.considerError(lastError, None)
                            self._trace(' =', (6983, 6985), self.input.position)
                            _G_apply_850, lastError = self._apply(self.rule_S, "S", [])
                            self.considerError(lastError, None)
                            _G_python_851, lastError = ("contains"), None
                            self.considerError(lastError, None)
                            return (_G_python_851, self.currentError)
                        _G_or_852, lastError = self._or([_G_or_806, _G_or_810, _G_or_815, _G_or_829, _G_or_841])
                        self.considerError(lastError, None)
                        _locals['operator'] = _G_or_852
                        self._trace('   ', (7027, 7030), self.input.position)
                        _G_apply_853, lastError = self._apply(self.rule_WS, "WS", [])
                        self.considerError(lastError, None)
                        self._trace('            ', (7030, 7042), self.input.position)
                        _G_apply_854, lastError = self._apply(self.rule_Expression2, "Expression2", [])
                        self.considerError(lastError, None)
                        _locals['ex2'] = _G_apply_854
                        _G_python_856, lastError = eval(self._G_expr_855, self.globals, _locals), None
                        self.considerError(lastError, None)
                        return (_G_python_856, self.currentError)
                    def _G_or_857():
                        self._trace('ert', (7083, 7086), self.input.position)
                        _G_apply_858, lastError = self._apply(self.rule_SP, "SP", [])
                        self.considerError(lastError, None)
                        self._trace('yL', (7086, 7088), self.input.position)
                        _G_apply_859, lastError = self._apply(self.rule_I, "I", [])
                        self.considerError(lastError, None)
                        self._trace('oo', (7088, 7090), self.input.position)
                        _G_apply_860, lastError = self._apply(self.rule_S, "S", [])
                        self.considerError(lastError, None)
                        self._trace('kup', (7090, 7093), self.input.position)
                        _G_apply_861, lastError = self._apply(self.rule_SP, "SP", [])
                        self.considerError(lastError, None)
                        self._trace('",', (7093, 7095), self.input.position)
                        _G_apply_862, lastError = self._apply(self.rule_N, "N", [])
                        self.considerError(lastError, None)
                        self._trace(' p', (7095, 7097), self.input.position)
                        _G_apply_863, lastError = self._apply(self.rule_U, "U", [])
                        self.considerError(lastError, None)
                        self._trace('ro', (7097, 7099), self.input.position)
                        _G_apply_864, lastError = self._apply(self.rule_L, "L", [])
                        self.considerError(lastError, None)
                        self._trace('p_', (7099, 7101), self.input.position)
                        _G_apply_865, lastError = self._apply(self.rule_L, "L", [])
                        self.considerError(lastError, None)
                        _G_python_866, lastError = (["is_null"]), None
                        self.considerError(lastError, None)
                        return (_G_python_866, self.currentError)
                    def _G_or_867():
                        self._trace(' Ex', (7135, 7138), self.input.position)
                        _G_apply_868, lastError = self._apply(self.rule_SP, "SP", [])
                        self.considerError(lastError, None)
                        self._trace('pr', (7138, 7140), self.input.position)
                        _G_apply_869, lastError = self._apply(self.rule_I, "I", [])
                        self.considerError(lastError, None)
                        self._trace('es', (7140, 7142), self.input.position)
                        _G_apply_870, lastError = self._apply(self.rule_S, "S", [])
                        self.considerError(lastError, None)
                        self._trace('sio', (7142, 7145), self.input.position)
                        _G_apply_871, lastError = self._apply(self.rule_SP, "SP", [])
                        self.considerError(lastError, None)
                        self._trace('n?', (7145, 7147), self.input.position)
                        _G_apply_872, lastError = self._apply(self.rule_N, "N", [])
                        self.considerError(lastError, None)
                        self._trace(':s', (7147, 7149), self.input.position)
                        _G_apply_873, lastError = self._apply(self.rule_O, "O", [])
                        self.considerError(lastError, None)
                        self._trace('ta', (7149, 7151), self.input.position)
                        _G_apply_874, lastError = self._apply(self.rule_T, "T", [])
                        self.considerError(lastError, None)
                        self._trace('rt ', (7151, 7154), self.input.position)
                        _G_apply_875, lastError = self._apply(self.rule_SP, "SP", [])
                        self.considerError(lastError, None)
                        self._trace("'.", (7154, 7156), self.input.position)
                        _G_apply_876, lastError = self._apply(self.rule_N, "N", [])
                        self.considerError(lastError, None)
                        self._trace(".'", (7156, 7158), self.input.position)
                        _G_apply_877, lastError = self._apply(self.rule_U, "U", [])
                        self.considerError(lastError, None)
                        self._trace(' E', (7158, 7160), self.input.position)
                        _G_apply_878, lastError = self._apply(self.rule_L, "L", [])
                        self.considerError(lastError, None)
                        self._trace('xp', (7160, 7162), self.input.position)
                        _G_apply_879, lastError = self._apply(self.rule_L, "L", [])
                        self.considerError(lastError, None)
                        _G_python_880, lastError = (["is_not_null"]), None
                        self.considerError(lastError, None)
                        return (_G_python_880, self.currentError)
                    _G_or_881, lastError = self._or([_G_or_783, _G_or_790, _G_or_805, _G_or_857, _G_or_867])
                    self.considerError(lastError, None)
                    return (_G_or_881, self.currentError)
                _G_many1_882, lastError = self.many(_G_many1_782, _G_many1_782())
                self.considerError(lastError, None)
                _locals['c'] = _G_many1_882
                _G_python_884, lastError = eval(self._G_expr_883, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_884, self.currentError)
            def _G_or_885():
                self._trace('         WS ', (7243, 7255), self.input.position)
                _G_apply_886, lastError = self._apply(self.rule_Expression2, "Expression2", [])
                self.considerError(lastError, None)
                return (_G_apply_886, self.currentError)
            _G_or_887, lastError = self._or([_G_or_780, _G_or_885])
            self.considerError(lastError, 'Expression3')
            return (_G_or_887, self.currentError)


        def rule_Expression2(self):
            _locals = {'self': self}
            self.locals['Expression2'] = _locals
            def _G_or_888():
                self._trace('\n    ', (7270, 7275), self.input.position)
                _G_apply_889, lastError = self._apply(self.rule_Atom, "Atom", [])
                self.considerError(lastError, None)
                _locals['a'] = _G_apply_889
                def _G_many1_890():
                    def _G_or_891():
                        self._trace('              ', (7279, 7293), self.input.position)
                        _G_apply_892, lastError = self._apply(self.rule_PropertyLookup, "PropertyLookup", [])
                        self.considerError(lastError, None)
                        return (_G_apply_892, self.currentError)
                    def _G_or_893():
                        self._trace('| SP I N ->', (7295, 7306), self.input.position)
                        _G_apply_894, lastError = self._apply(self.rule_NodeLabels, "NodeLabels", [])
                        self.considerError(lastError, None)
                        return (_G_apply_894, self.currentError)
                    _G_or_895, lastError = self._or([_G_or_891, _G_or_893])
                    self.considerError(lastError, None)
                    return (_G_or_895, self.currentError)
                _G_many1_896, lastError = self.many(_G_many1_890, _G_many1_890())
                self.considerError(lastError, None)
                _locals['c'] = _G_many1_896
                _G_python_898, lastError = eval(self._G_expr_897, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_898, self.currentError)
            def _G_or_899():
                self._trace('S SP ', (7351, 7356), self.input.position)
                _G_apply_900, lastError = self._apply(self.rule_Atom, "Atom", [])
                self.considerError(lastError, None)
                return (_G_apply_900, self.currentError)
            _G_or_901, lastError = self._or([_G_or_888, _G_or_899])
            self.considerError(lastError, 'Expression2')
            return (_G_or_901, self.currentError)


        def rule_Atom(self):
            _locals = {'self': self}
            self.locals['Atom'] = _locals
            def _G_or_902():
                self._trace('-> "starts_wit', (7364, 7378), self.input.position)
                _G_apply_903, lastError = self._apply(self.rule_NumberLiteral, "NumberLiteral", [])
                self.considerError(lastError, None)
                return (_G_apply_903, self.currentError)
            def _G_or_904():
                self._trace('              ', (7385, 7399), self.input.position)
                _G_apply_905, lastError = self._apply(self.rule_StringLiteral, "StringLiteral", [])
                self.considerError(lastError, None)
                return (_G_apply_905, self.currentError)
            def _G_or_906():
                self._trace(' SP E N D ', (7406, 7416), self.input.position)
                _G_apply_907, lastError = self._apply(self.rule_Parameter, "Parameter", [])
                self.considerError(lastError, None)
                return (_G_apply_907, self.currentError)
            def _G_or_908():
                self._trace('I ', (7423, 7425), self.input.position)
                _G_apply_909, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                self._trace('T ', (7425, 7427), self.input.position)
                _G_apply_910, lastError = self._apply(self.rule_R, "R", [])
                self.considerError(lastError, None)
                self._trace('H ', (7427, 7429), self.input.position)
                _G_apply_911, lastError = self._apply(self.rule_U, "U", [])
                self.considerError(lastError, None)
                self._trace(' -', (7429, 7431), self.input.position)
                _G_apply_912, lastError = self._apply(self.rule_E, "E", [])
                self.considerError(lastError, None)
                _G_python_913, lastError = (["Literal", True]), None
                self.considerError(lastError, None)
                return (_G_python_913, self.currentError)
            def _G_or_914():
                self._trace('  ', (7459, 7461), self.input.position)
                _G_apply_915, lastError = self._apply(self.rule_F, "F", [])
                self.considerError(lastError, None)
                self._trace('  ', (7461, 7463), self.input.position)
                _G_apply_916, lastError = self._apply(self.rule_A, "A", [])
                self.considerError(lastError, None)
                self._trace('  ', (7463, 7465), self.input.position)
                _G_apply_917, lastError = self._apply(self.rule_L, "L", [])
                self.considerError(lastError, None)
                self._trace('  ', (7465, 7467), self.input.position)
                _G_apply_918, lastError = self._apply(self.rule_S, "S", [])
                self.considerError(lastError, None)
                self._trace('  ', (7467, 7469), self.input.position)
                _G_apply_919, lastError = self._apply(self.rule_E, "E", [])
                self.considerError(lastError, None)
                _G_python_920, lastError = (["Literal", False]), None
                self.considerError(lastError, None)
                return (_G_python_920, self.currentError)
            def _G_or_921():
                self._trace('ta', (7498, 7500), self.input.position)
                _G_apply_922, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace('in', (7500, 7502), self.input.position)
                _G_apply_923, lastError = self._apply(self.rule_U, "U", [])
                self.considerError(lastError, None)
                self._trace('s"', (7502, 7504), self.input.position)
                _G_apply_924, lastError = self._apply(self.rule_L, "L", [])
                self.considerError(lastError, None)
                self._trace('\n ', (7504, 7506), self.input.position)
                _G_apply_925, lastError = self._apply(self.rule_L, "L", [])
                self.considerError(lastError, None)
                _G_python_926, lastError = (["Literal", None]), None
                self.considerError(lastError, None)
                return (_G_python_926, self.currentError)
            def _G_or_927():
                self._trace('r WS Expression', (7534, 7549), self.input.position)
                _G_apply_928, lastError = self._apply(self.rule_CaseExpression, "CaseExpression", [])
                self.considerError(lastError, None)
                return (_G_apply_928, self.currentError)
            def _G_or_929():
                self._trace('> ', (7556, 7558), self.input.position)
                _G_apply_930, lastError = self._apply(self.rule_C, "C", [])
                self.considerError(lastError, None)
                self._trace('[o', (7558, 7560), self.input.position)
                _G_apply_931, lastError = self._apply(self.rule_O, "O", [])
                self.considerError(lastError, None)
                self._trace('pe', (7560, 7562), self.input.position)
                _G_apply_932, lastError = self._apply(self.rule_U, "U", [])
                self.considerError(lastError, None)
                self._trace('ra', (7562, 7564), self.input.position)
                _G_apply_933, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace('to', (7564, 7566), self.input.position)
                _G_apply_934, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                self._trace('r, e', (7566, 7570), self.input.position)
                _G_exactly_935, lastError = self.exactly('(')
                self.considerError(lastError, None)
                self._trace('x2]\n', (7570, 7574), self.input.position)
                _G_exactly_936, lastError = self.exactly('*')
                self.considerError(lastError, None)
                self._trace('    ', (7574, 7578), self.input.position)
                _G_exactly_937, lastError = self.exactly(')')
                self.considerError(lastError, None)
                _G_python_938, lastError = (["count *"]), None
                self.considerError(lastError, None)
                return (_G_python_938, self.currentError)
            def _G_or_939():
                self._trace(' S SP N U L', (7600, 7611), self.input.position)
                _G_apply_940, lastError = self._apply(self.rule_MapLiteral, "MapLiteral", [])
                self.considerError(lastError, None)
                return (_G_apply_940, self.currentError)
            def _G_or_941():
                self._trace('["is_null"]\n      ', (7618, 7636), self.input.position)
                _G_apply_942, lastError = self._apply(self.rule_ListComprehension, "ListComprehension", [])
                self.considerError(lastError, None)
                return (_G_apply_942, self.currentError)
            def _G_or_943():
                self._trace('    ', (7643, 7647), self.input.position)
                _G_exactly_944, lastError = self.exactly('[')
                self.considerError(lastError, None)
                def _G_or_945():
                    self._trace(' N O T SP N U L L -', (7661, 7680), self.input.position)
                    _G_apply_946, lastError = self._apply(self.rule_WS, "WS", [])
                    self.considerError(lastError, None)
                    self._trace('> ["is_not_', (7680, 7691), self.input.position)
                    _G_apply_947, lastError = self._apply(self.rule_Expression, "Expression", [])
                    self.considerError(lastError, None)
                    _locals['head'] = _G_apply_947
                    self._trace(']\n ', (7696, 7699), self.input.position)
                    _G_apply_948, lastError = self._apply(self.rule_WS, "WS", [])
                    self.considerError(lastError, None)
                    def _G_many_949():
                        self._trace('+:c', (7717, 7720), self.input.position)
                        _G_exactly_950, lastError = self.exactly(',')
                        self.considerError(lastError, None)
                        self._trace(' ->', (7720, 7723), self.input.position)
                        _G_apply_951, lastError = self._apply(self.rule_WS, "WS", [])
                        self.considerError(lastError, None)
                        self._trace(' ["Expressi', (7723, 7734), self.input.position)
                        _G_apply_952, lastError = self._apply(self.rule_Expression, "Expression", [])
                        self.considerError(lastError, None)
                        _locals['item'] = _G_apply_952
                        self._trace(' ex', (7739, 7742), self.input.position)
                        _G_apply_953, lastError = self._apply(self.rule_WS, "WS", [])
                        self.considerError(lastError, None)
                        _G_python_955, lastError = eval(self._G_expr_954, self.globals, _locals), None
                        self.considerError(lastError, None)
                        return (_G_python_955, self.currentError)
                    _G_many_956, lastError = self.many(_G_many_949)
                    self.considerError(lastError, None)
                    _locals['tail'] = _G_many_956
                    _G_python_957, lastError = eval(self._G_expr_442, self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_957, self.currentError)
                def _G_or_958():
                    _G_python_959, lastError = ([]), None
                    self.considerError(lastError, None)
                    return (_G_python_959, self.currentError)
                _G_or_960, lastError = self._or([_G_or_945, _G_or_958])
                self.considerError(lastError, None)
                _locals['ex'] = _G_or_960
                self._trace('ession2", a,', (7848, 7860), self.input.position)
                _G_exactly_961, lastError = self.exactly(']')
                self.considerError(lastError, None)
                _G_python_963, lastError = eval(self._G_expr_962, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_963, self.currentError)
            def _G_or_964():
                self._trace(' A', (7883, 7885), self.input.position)
                _G_apply_965, lastError = self._apply(self.rule_F, "F", [])
                self.considerError(lastError, None)
                self._trace('to', (7885, 7887), self.input.position)
                _G_apply_966, lastError = self._apply(self.rule_I, "I", [])
                self.considerError(lastError, None)
                self._trace('m\n', (7887, 7889), self.input.position)
                _G_apply_967, lastError = self._apply(self.rule_L, "L", [])
                self.considerError(lastError, None)
                self._trace('\n ', (7889, 7891), self.input.position)
                _G_apply_968, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                self._trace('  ', (7891, 7893), self.input.position)
                _G_apply_969, lastError = self._apply(self.rule_E, "E", [])
                self.considerError(lastError, None)
                self._trace(' A', (7893, 7895), self.input.position)
                _G_apply_970, lastError = self._apply(self.rule_R, "R", [])
                self.considerError(lastError, None)
                self._trace('tom', (7895, 7898), self.input.position)
                _G_apply_971, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace(' = N', (7898, 7902), self.input.position)
                _G_exactly_972, lastError = self.exactly('(')
                self.considerError(lastError, None)
                self._trace('umb', (7902, 7905), self.input.position)
                _G_apply_973, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('erLiteral\n       ', (7905, 7922), self.input.position)
                _G_apply_974, lastError = self._apply(self.rule_FilterExpression, "FilterExpression", [])
                self.considerError(lastError, None)
                _locals['fex'] = _G_apply_974
                self._trace('Str', (7926, 7929), self.input.position)
                _G_apply_975, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('ingL', (7929, 7933), self.input.position)
                _G_exactly_976, lastError = self.exactly(')')
                self.considerError(lastError, None)
                _G_python_978, lastError = eval(self._G_expr_977, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_978, self.currentError)
            def _G_or_979():
                self._trace('r\n', (7959, 7961), self.input.position)
                _G_apply_980, lastError = self._apply(self.rule_E, "E", [])
                self.considerError(lastError, None)
                self._trace('  ', (7961, 7963), self.input.position)
                _G_apply_981, lastError = self._apply(self.rule_X, "X", [])
                self.considerError(lastError, None)
                self._trace('  ', (7963, 7965), self.input.position)
                _G_apply_982, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                self._trace('  ', (7965, 7967), self.input.position)
                _G_apply_983, lastError = self._apply(self.rule_R, "R", [])
                self.considerError(lastError, None)
                self._trace('  ', (7967, 7969), self.input.position)
                _G_apply_984, lastError = self._apply(self.rule_A, "A", [])
                self.considerError(lastError, None)
                self._trace(' |', (7969, 7971), self.input.position)
                _G_apply_985, lastError = self._apply(self.rule_C, "C", [])
                self.considerError(lastError, None)
                self._trace(' T', (7971, 7973), self.input.position)
                _G_apply_986, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                self._trace(' R ', (7973, 7976), self.input.position)
                _G_apply_987, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('U E ', (7976, 7980), self.input.position)
                _G_exactly_988, lastError = self.exactly('(')
                self.considerError(lastError, None)
                self._trace('-> ', (7980, 7983), self.input.position)
                _G_apply_989, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('["Literal", True]', (7983, 8000), self.input.position)
                _G_apply_990, lastError = self._apply(self.rule_FilterExpression, "FilterExpression", [])
                self.considerError(lastError, None)
                _locals['fex'] = _G_apply_990
                self._trace('   ', (8004, 8007), self.input.position)
                _G_apply_991, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                def _G_optional_992():
                    self._trace(' |', (8009, 8011), self.input.position)
                    _G_apply_993, lastError = self._apply(self.rule_WS, "WS", [])
                    self.considerError(lastError, None)
                    self._trace(' F A', (8011, 8015), self.input.position)
                    _G_exactly_994, lastError = self.exactly('|')
                    self.considerError(lastError, None)
                    self._trace(' L S E -> [', (8015, 8026), self.input.position)
                    _G_apply_995, lastError = self._apply(self.rule_Expression, "Expression", [])
                    self.considerError(lastError, None)
                    return (_G_apply_995, self.currentError)
                def _G_optional_996():
                    return (None, self.input.nullError())
                _G_or_997, lastError = self._or([_G_optional_992, _G_optional_996])
                self.considerError(lastError, None)
                _locals['ex'] = _G_or_997
                self._trace('ral"', (8031, 8035), self.input.position)
                _G_exactly_998, lastError = self.exactly(')')
                self.considerError(lastError, None)
                _G_python_1000, lastError = eval(self._G_expr_999, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_1000, self.currentError)
            def _G_or_1001():
                self._trace('["', (8066, 8068), self.input.position)
                _G_apply_1002, lastError = self._apply(self.rule_A, "A", [])
                self.considerError(lastError, None)
                self._trace('Li', (8068, 8070), self.input.position)
                _G_apply_1003, lastError = self._apply(self.rule_L, "L", [])
                self.considerError(lastError, None)
                self._trace('te', (8070, 8072), self.input.position)
                _G_apply_1004, lastError = self._apply(self.rule_L, "L", [])
                self.considerError(lastError, None)
                self._trace('ral', (8072, 8075), self.input.position)
                _G_apply_1005, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('", N', (8075, 8079), self.input.position)
                _G_exactly_1006, lastError = self.exactly('(')
                self.considerError(lastError, None)
                self._trace('one', (8079, 8082), self.input.position)
                _G_apply_1007, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace(']\n         | Case', (8082, 8099), self.input.position)
                _G_apply_1008, lastError = self._apply(self.rule_FilterExpression, "FilterExpression", [])
                self.considerError(lastError, None)
                _locals['fex'] = _G_apply_1008
                self._trace('ess', (8103, 8106), self.input.position)
                _G_apply_1009, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('ion\n', (8106, 8110), self.input.position)
                _G_exactly_1010, lastError = self.exactly(')')
                self.considerError(lastError, None)
                _G_python_1012, lastError = eval(self._G_expr_1011, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_1012, self.currentError)
            def _G_or_1013():
                self._trace("' ", (8133, 8135), self.input.position)
                _G_apply_1014, lastError = self._apply(self.rule_A, "A", [])
                self.considerError(lastError, None)
                self._trace("'*", (8135, 8137), self.input.position)
                _G_apply_1015, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace("' ", (8137, 8139), self.input.position)
                _G_apply_1016, lastError = self._apply(self.rule_Y, "Y", [])
                self.considerError(lastError, None)
                self._trace("')'", (8139, 8142), self.input.position)
                _G_apply_1017, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace(' -> ', (8142, 8146), self.input.position)
                _G_exactly_1018, lastError = self.exactly('(')
                self.considerError(lastError, None)
                self._trace('["c', (8146, 8149), self.input.position)
                _G_apply_1019, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('ount *"]\n        ', (8149, 8166), self.input.position)
                _G_apply_1020, lastError = self._apply(self.rule_FilterExpression, "FilterExpression", [])
                self.considerError(lastError, None)
                _locals['fex'] = _G_apply_1020
                self._trace('apL', (8170, 8173), self.input.position)
                _G_apply_1021, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('iter', (8173, 8177), self.input.position)
                _G_exactly_1022, lastError = self.exactly(')')
                self.considerError(lastError, None)
                _G_python_1024, lastError = eval(self._G_expr_1023, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_1024, self.currentError)
            def _G_or_1025():
                self._trace('eh', (8200, 8202), self.input.position)
                _G_apply_1026, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace('en', (8202, 8204), self.input.position)
                _G_apply_1027, lastError = self._apply(self.rule_O, "O", [])
                self.considerError(lastError, None)
                self._trace('si', (8204, 8206), self.input.position)
                _G_apply_1028, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace('on', (8206, 8208), self.input.position)
                _G_apply_1029, lastError = self._apply(self.rule_E, "E", [])
                self.considerError(lastError, None)
                self._trace('\n  ', (8208, 8211), self.input.position)
                _G_apply_1030, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('    ', (8211, 8215), self.input.position)
                _G_exactly_1031, lastError = self.exactly('(')
                self.considerError(lastError, None)
                self._trace('   ', (8215, 8218), self.input.position)
                _G_apply_1032, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace("| '['\n           ", (8218, 8235), self.input.position)
                _G_apply_1033, lastError = self._apply(self.rule_FilterExpression, "FilterExpression", [])
                self.considerError(lastError, None)
                _locals['fex'] = _G_apply_1033
                self._trace(' (\n', (8239, 8242), self.input.position)
                _G_apply_1034, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('    ', (8242, 8246), self.input.position)
                _G_exactly_1035, lastError = self.exactly(')')
                self.considerError(lastError, None)
                _G_python_1037, lastError = eval(self._G_expr_1036, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_1037, self.currentError)
            def _G_or_1038():
                self._trace('ss', (8270, 8272), self.input.position)
                _G_apply_1039, lastError = self._apply(self.rule_S, "S", [])
                self.considerError(lastError, None)
                self._trace('io', (8272, 8274), self.input.position)
                _G_apply_1040, lastError = self._apply(self.rule_I, "I", [])
                self.considerError(lastError, None)
                self._trace('n:', (8274, 8276), self.input.position)
                _G_apply_1041, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace('he', (8276, 8278), self.input.position)
                _G_apply_1042, lastError = self._apply(self.rule_G, "G", [])
                self.considerError(lastError, None)
                self._trace('ad', (8278, 8280), self.input.position)
                _G_apply_1043, lastError = self._apply(self.rule_L, "L", [])
                self.considerError(lastError, None)
                self._trace(' W', (8280, 8282), self.input.position)
                _G_apply_1044, lastError = self._apply(self.rule_E, "E", [])
                self.considerError(lastError, None)
                self._trace('S\n ', (8282, 8285), self.input.position)
                _G_apply_1045, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('    ', (8285, 8289), self.input.position)
                _G_exactly_1046, lastError = self.exactly('(')
                self.considerError(lastError, None)
                self._trace('   ', (8289, 8292), self.input.position)
                _G_apply_1047, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace("            (',' ", (8292, 8309), self.input.position)
                _G_apply_1048, lastError = self._apply(self.rule_FilterExpression, "FilterExpression", [])
                self.considerError(lastError, None)
                _locals['fex'] = _G_apply_1048
                self._trace('xpr', (8313, 8316), self.input.position)
                _G_apply_1049, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('essi', (8316, 8320), self.input.position)
                _G_exactly_1050, lastError = self.exactly(')')
                self.considerError(lastError, None)
                _G_python_1052, lastError = eval(self._G_expr_1051, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_1052, self.currentError)
            def _G_or_1053():
                self._trace('             )*:tail ', (8346, 8367), self.input.position)
                _G_apply_1054, lastError = self._apply(self.rule_RelationshipsPattern, "RelationshipsPattern", [])
                self.considerError(lastError, None)
                return (_G_apply_1054, self.currentError)
            def _G_or_1055():
                self._trace('d] + tail\n                ', (8374, 8400), self.input.position)
                _G_apply_1056, lastError = self._apply(self.rule_GraphRelationshipsPattern, "GraphRelationshipsPattern", [])
                self.considerError(lastError, None)
                return (_G_apply_1056, self.currentError)
            def _G_or_1057():
                self._trace('                   -> []', (8407, 8431), self.input.position)
                _G_apply_1058, lastError = self._apply(self.rule_parenthesizedExpression, "parenthesizedExpression", [])
                self.considerError(lastError, None)
                return (_G_apply_1058, self.currentError)
            def _G_or_1059():
                self._trace('          ):ex\n    ', (8438, 8457), self.input.position)
                _G_apply_1060, lastError = self._apply(self.rule_FunctionInvocation, "FunctionInvocation", [])
                self.considerError(lastError, None)
                return (_G_apply_1060, self.currentError)
            def _G_or_1061():
                self._trace(" ']' -> [", (8464, 8473), self.input.position)
                _G_apply_1062, lastError = self._apply(self.rule_Variable, "Variable", [])
                self.considerError(lastError, None)
                return (_G_apply_1062, self.currentError)
            _G_or_1063, lastError = self._or([_G_or_902, _G_or_904, _G_or_906, _G_or_908, _G_or_914, _G_or_921, _G_or_927, _G_or_929, _G_or_939, _G_or_941, _G_or_943, _G_or_964, _G_or_979, _G_or_1001, _G_or_1013, _G_or_1025, _G_or_1038, _G_or_1053, _G_or_1055, _G_or_1057, _G_or_1059, _G_or_1061])
            self.considerError(lastError, 'Atom')
            return (_G_or_1063, self.currentError)


        def rule_parenthesizedExpression(self):
            _locals = {'self': self}
            self.locals['parenthesizedExpression'] = _locals
            self._trace('L T ', (8500, 8504), self.input.position)
            _G_exactly_1064, lastError = self.exactly('(')
            self.considerError(lastError, 'parenthesizedExpression')
            self._trace('E R', (8504, 8507), self.input.position)
            _G_apply_1065, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'parenthesizedExpression')
            self._trace(" WS '(' WS ", (8507, 8518), self.input.position)
            _G_apply_1066, lastError = self._apply(self.rule_Expression, "Expression", [])
            self.considerError(lastError, 'parenthesizedExpression')
            _locals['ex'] = _G_apply_1066
            self._trace('ter', (8521, 8524), self.input.position)
            _G_apply_1067, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'parenthesizedExpression')
            self._trace('Expr', (8524, 8528), self.input.position)
            _G_exactly_1068, lastError = self.exactly(')')
            self.considerError(lastError, 'parenthesizedExpression')
            _G_python_1070, lastError = eval(self._G_expr_1069, self.globals, _locals), None
            self.considerError(lastError, 'parenthesizedExpression')
            return (_G_python_1070, self.currentError)


        def rule_RelationshipsPattern(self):
            _locals = {'self': self}
            self.locals['RelationshipsPattern'] = _locals
            self._trace(', fex]\n     ', (8558, 8570), self.input.position)
            _G_apply_1071, lastError = self._apply(self.rule_NodePattern, "NodePattern", [])
            self.considerError(lastError, 'RelationshipsPattern')
            _locals['np'] = _G_apply_1071
            def _G_optional_1072():
                self._trace(' E', (8575, 8577), self.input.position)
                _G_apply_1073, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace(" X T R A C T WS '(' ", (8577, 8597), self.input.position)
                _G_apply_1074, lastError = self._apply(self.rule_PatternElementChain, "PatternElementChain", [])
                self.considerError(lastError, None)
                return (_G_apply_1074, self.currentError)
            def _G_optional_1075():
                return (None, self.input.nullError())
            _G_or_1076, lastError = self._or([_G_optional_1072, _G_optional_1075])
            self.considerError(lastError, 'RelationshipsPattern')
            _locals['pec'] = _G_or_1076
            _G_python_1078, lastError = eval(self._G_expr_1077, self.globals, _locals), None
            self.considerError(lastError, 'RelationshipsPattern')
            return (_G_python_1078, self.currentError)


        def rule_GraphRelationshipsPattern(self):
            _locals = {'self': self}
            self.locals['GraphRelationshipsPattern'] = _locals
            self._trace('x, ex]\n  ', (8669, 8678), self.input.position)
            _G_apply_1079, lastError = self._apply(self.rule_Variable, "Variable", [])
            self.considerError(lastError, 'GraphRelationshipsPattern')
            _locals['v'] = _G_apply_1079
            self._trace('    ', (8680, 8684), self.input.position)
            _G_exactly_1080, lastError = self.exactly(':')
            self.considerError(lastError, 'GraphRelationshipsPattern')
            self._trace(' | ', (8684, 8687), self.input.position)
            _G_apply_1081, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'GraphRelationshipsPattern')
            self._trace("A L L WS '('", (8687, 8699), self.input.position)
            _G_apply_1082, lastError = self._apply(self.rule_NodePattern, "NodePattern", [])
            self.considerError(lastError, 'GraphRelationshipsPattern')
            _locals['np'] = _G_apply_1082
            def _G_optional_1083():
                self._trace('il', (8704, 8706), self.input.position)
                _G_apply_1084, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('terExpression:fex WS', (8706, 8726), self.input.position)
                _G_apply_1085, lastError = self._apply(self.rule_PatternElementChain, "PatternElementChain", [])
                self.considerError(lastError, None)
                return (_G_apply_1085, self.currentError)
            def _G_optional_1086():
                return (None, self.input.nullError())
            _G_or_1087, lastError = self._or([_G_optional_1083, _G_optional_1086])
            self.considerError(lastError, 'GraphRelationshipsPattern')
            _locals['pec'] = _G_or_1087
            _G_python_1089, lastError = eval(self._G_expr_1088, self.globals, _locals), None
            self.considerError(lastError, 'GraphRelationshipsPattern')
            return (_G_python_1089, self.currentError)


        def rule_FilterExpression(self):
            _locals = {'self': self}
            self.locals['FilterExpression'] = _locals
            self._trace(" ')' -> [", (8797, 8806), self.input.position)
            _G_apply_1090, lastError = self._apply(self.rule_IdInColl, "IdInColl", [])
            self.considerError(lastError, 'FilterExpression')
            _locals['i'] = _G_apply_1090
            def _G_optional_1091():
                self._trace('",', (8810, 8812), self.input.position)
                _G_apply_1092, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace(' fex]\n', (8812, 8818), self.input.position)
                _G_apply_1093, lastError = self._apply(self.rule_Where, "Where", [])
                self.considerError(lastError, None)
                return (_G_apply_1093, self.currentError)
            def _G_optional_1094():
                return (None, self.input.nullError())
            _G_or_1095, lastError = self._or([_G_optional_1091, _G_optional_1094])
            self.considerError(lastError, 'FilterExpression')
            _locals['w'] = _G_or_1095
            _G_python_1097, lastError = eval(self._G_expr_1096, self.globals, _locals), None
            self.considerError(lastError, 'FilterExpression')
            return (_G_python_1097, self.currentError)


        def rule_IdInColl(self):
            _locals = {'self': self}
            self.locals['IdInColl'] = _locals
            self._trace("fex WS ')", (8864, 8873), self.input.position)
            _G_apply_1098, lastError = self._apply(self.rule_Variable, "Variable", [])
            self.considerError(lastError, 'IdInColl')
            _locals['v'] = _G_apply_1098
            self._trace('-> ', (8875, 8878), self.input.position)
            _G_apply_1099, lastError = self._apply(self.rule_SP, "SP", [])
            self.considerError(lastError, 'IdInColl')
            self._trace('["', (8878, 8880), self.input.position)
            _G_apply_1100, lastError = self._apply(self.rule_I, "I", [])
            self.considerError(lastError, 'IdInColl')
            self._trace('No', (8880, 8882), self.input.position)
            _G_apply_1101, lastError = self._apply(self.rule_N, "N", [])
            self.considerError(lastError, 'IdInColl')
            self._trace('ne"', (8882, 8885), self.input.position)
            _G_apply_1102, lastError = self._apply(self.rule_SP, "SP", [])
            self.considerError(lastError, 'IdInColl')
            self._trace(', fex]\n    ', (8885, 8896), self.input.position)
            _G_apply_1103, lastError = self._apply(self.rule_Expression, "Expression", [])
            self.considerError(lastError, 'IdInColl')
            _locals['ex'] = _G_apply_1103
            _G_python_1105, lastError = eval(self._G_expr_1104, self.globals, _locals), None
            self.considerError(lastError, 'IdInColl')
            return (_G_python_1105, self.currentError)


        def rule_FunctionInvocation(self):
            _locals = {'self': self}
            self.locals['FunctionInvocation'] = _locals
            self._trace("x WS ')' -> [", (8944, 8957), self.input.position)
            _G_apply_1106, lastError = self._apply(self.rule_FunctionName, "FunctionName", [])
            self.considerError(lastError, 'FunctionInvocation')
            _locals['func'] = _G_apply_1106
            self._trace('le", fex]\n         | Re', (8962, 8985), self.input.position)
            _G_apply_1107, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'FunctionInvocation')
            self._trace('lati', (8985, 8989), self.input.position)
            _G_exactly_1108, lastError = self.exactly('(')
            self.considerError(lastError, 'FunctionInvocation')
            self._trace('ons', (8989, 8992), self.input.position)
            _G_apply_1109, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'FunctionInvocation')
            def _G_optional_1110():
                self._trace(' ', (9014, 9015), self.input.position)
                _G_apply_1111, lastError = self._apply(self.rule_D, "D", [])
                self.considerError(lastError, None)
                self._trace('Gr', (9015, 9017), self.input.position)
                _G_apply_1112, lastError = self._apply(self.rule_I, "I", [])
                self.considerError(lastError, None)
                self._trace('ap', (9017, 9019), self.input.position)
                _G_apply_1113, lastError = self._apply(self.rule_S, "S", [])
                self.considerError(lastError, None)
                self._trace('hR', (9019, 9021), self.input.position)
                _G_apply_1114, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                self._trace('el', (9021, 9023), self.input.position)
                _G_apply_1115, lastError = self._apply(self.rule_I, "I", [])
                self.considerError(lastError, None)
                self._trace('at', (9023, 9025), self.input.position)
                _G_apply_1116, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace('io', (9025, 9027), self.input.position)
                _G_apply_1117, lastError = self._apply(self.rule_C, "C", [])
                self.considerError(lastError, None)
                self._trace('ns', (9027, 9029), self.input.position)
                _G_apply_1118, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                self._trace('hip', (9029, 9032), self.input.position)
                _G_apply_1119, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                _G_python_1120, lastError = ("distinct"), None
                self.considerError(lastError, None)
                return (_G_python_1120, self.currentError)
            def _G_optional_1121():
                return (None, self.input.nullError())
            _G_or_1122, lastError = self._or([_G_optional_1110, _G_optional_1121])
            self.considerError(lastError, 'FunctionInvocation')
            _locals['distinct'] = _G_or_1122
            def _G_or_1123():
                self._trace('      | FunctionInvocation\n        ', (9079, 9114), self.input.position)
                _G_apply_1124, lastError = self._apply(self.rule_Expression, "Expression", [])
                self.considerError(lastError, None)
                _locals['head'] = _G_apply_1124
                def _G_many_1125():
                    self._trace("xpression = '(' WS Expression:ex", (9145, 9177), self.input.position)
                    _G_exactly_1126, lastError = self.exactly(',')
                    self.considerError(lastError, None)
                    self._trace(' WS', (9177, 9180), self.input.position)
                    _G_apply_1127, lastError = self._apply(self.rule_WS, "WS", [])
                    self.considerError(lastError, None)
                    self._trace(" ')' -> ex\n", (9180, 9191), self.input.position)
                    _G_apply_1128, lastError = self._apply(self.rule_Expression, "Expression", [])
                    self.considerError(lastError, None)
                    return (_G_apply_1128, self.currentError)
                _G_many_1129, lastError = self.many(_G_many_1125)
                self.considerError(lastError, None)
                _locals['tail'] = _G_many_1129
                _G_python_1130, lastError = eval(self._G_expr_442, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_1130, self.currentError)
            def _G_or_1131():
                _G_python_1132, lastError = ([]), None
                self.considerError(lastError, None)
                return (_G_python_1132, self.currentError)
            _G_or_1133, lastError = self._or([_G_or_1123, _G_or_1131])
            self.considerError(lastError, 'FunctionInvocation')
            _locals['args'] = _G_or_1133
            self._trace(' pec]\n    \n    GraphRel', (9295, 9318), self.input.position)
            _G_apply_1134, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'FunctionInvocation')
            self._trace('atio', (9318, 9322), self.input.position)
            _G_exactly_1135, lastError = self.exactly(')')
            self.considerError(lastError, 'FunctionInvocation')
            _G_python_1137, lastError = eval(self._G_expr_1136, self.globals, _locals), None
            self.considerError(lastError, 'FunctionInvocation')
            return (_G_python_1137, self.currentError)


        def rule_FunctionName(self):
            _locals = {'self': self}
            self.locals['FunctionName'] = _locals
            self._trace('WS PatternEle', (9372, 9385), self.input.position)
            _G_apply_1138, lastError = self._apply(self.rule_SymbolicName, "SymbolicName", [])
            self.considerError(lastError, 'FunctionName')
            return (_G_apply_1138, self.currentError)


        def rule_ListComprehension(self):
            _locals = {'self': self}
            self.locals['ListComprehension'] = _locals
            self._trace('Grap', (9406, 9410), self.input.position)
            _G_exactly_1139, lastError = self.exactly('[')
            self.considerError(lastError, 'ListComprehension')
            self._trace('hRelationshipsPat', (9410, 9427), self.input.position)
            _G_apply_1140, lastError = self._apply(self.rule_FilterExpression, "FilterExpression", [])
            self.considerError(lastError, 'ListComprehension')
            _locals['fex'] = _G_apply_1140
            def _G_optional_1141():
                self._trace(' v', (9433, 9435), self.input.position)
                _G_apply_1142, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace(', np', (9435, 9439), self.input.position)
                _G_exactly_1143, lastError = self.exactly('|')
                self.considerError(lastError, None)
                self._trace(', pec]\n\n   ', (9439, 9450), self.input.position)
                _G_apply_1144, lastError = self._apply(self.rule_Expression, "Expression", [])
                self.considerError(lastError, None)
                return (_G_apply_1144, self.currentError)
            def _G_optional_1145():
                return (None, self.input.nullError())
            _G_or_1146, lastError = self._or([_G_optional_1141, _G_optional_1145])
            self.considerError(lastError, 'ListComprehension')
            _locals['ex'] = _G_or_1146
            self._trace('erEx', (9455, 9459), self.input.position)
            _G_exactly_1147, lastError = self.exactly(']')
            self.considerError(lastError, 'ListComprehension')
            _G_python_1149, lastError = eval(self._G_expr_1148, self.globals, _locals), None
            self.considerError(lastError, 'ListComprehension')
            return (_G_python_1149, self.currentError)


        def rule_PropertyLookup(self):
            _locals = {'self': self}
            self.locals['PropertyLookup'] = _locals
            self._trace(', v', (9590, 9593), self.input.position)
            _G_apply_1150, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'PropertyLookup')
            self._trace(', ex', (9593, 9597), self.input.position)
            _G_exactly_1151, lastError = self.exactly('.')
            self.considerError(lastError, 'PropertyLookup')
            self._trace(']\n\n', (9597, 9600), self.input.position)
            _G_apply_1152, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'PropertyLookup')
            self._trace('    FunctionInvo', (9600, 9616), self.input.position)
            _G_apply_1153, lastError = self._apply(self.rule_PropertyKeyName, "PropertyKeyName", [])
            self.considerError(lastError, 'PropertyLookup')
            _locals['n'] = _G_apply_1153
            _G_python_1155, lastError = eval(self._G_expr_1154, self.globals, _locals), None
            self.considerError(lastError, 'PropertyLookup')
            return (_G_python_1155, self.currentError)


        def rule_CaseExpression(self):
            _locals = {'self': self}
            self.locals['CaseExpression'] = _locals
            self._trace("      WS '(' WS\n   ", (9661, 9680), self.input.position)
            _G_apply_1156, lastError = self._apply(self.rule_C, "C", [])
            self.considerError(lastError, 'CaseExpression')
            self._trace('  ', (9680, 9682), self.input.position)
            _G_apply_1157, lastError = self._apply(self.rule_A, "A", [])
            self.considerError(lastError, 'CaseExpression')
            self._trace('  ', (9682, 9684), self.input.position)
            _G_apply_1158, lastError = self._apply(self.rule_S, "S", [])
            self.considerError(lastError, 'CaseExpression')
            self._trace('  ', (9684, 9686), self.input.position)
            _G_apply_1159, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'CaseExpression')
            self._trace('   ', (9686, 9689), self.input.position)
            _G_apply_1160, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'CaseExpression')
            def _G_optional_1161():
                self._trace('T I N C T ', (9708, 9718), self.input.position)
                _G_apply_1162, lastError = self._apply(self.rule_Expression, "Expression", [])
                self.considerError(lastError, None)
                return (_G_apply_1162, self.currentError)
            def _G_optional_1163():
                return (None, self.input.nullError())
            _G_or_1164, lastError = self._or([_G_optional_1161, _G_optional_1163])
            self.considerError(lastError, 'CaseExpression')
            _locals['ex'] = _G_or_1164
            def _G_many1_1165():
                self._trace('nc', (9742, 9744), self.input.position)
                _G_apply_1166, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('t\n               ', (9744, 9761), self.input.position)
                _G_apply_1167, lastError = self._apply(self.rule_CaseAlternatives, "CaseAlternatives", [])
                self.considerError(lastError, None)
                return (_G_apply_1167, self.currentError)
            _G_many1_1168, lastError = self.many(_G_many1_1165, _G_many1_1165())
            self.considerError(lastError, 'CaseExpression')
            _locals['cas'] = _G_many1_1168
            def _G_optional_1169():
                self._trace('  ', (9787, 9789), self.input.position)
                _G_apply_1170, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('  ', (9789, 9791), self.input.position)
                _G_apply_1171, lastError = self._apply(self.rule_E, "E", [])
                self.considerError(lastError, None)
                self._trace('  ', (9791, 9793), self.input.position)
                _G_apply_1172, lastError = self._apply(self.rule_L, "L", [])
                self.considerError(lastError, None)
                self._trace('  ', (9793, 9795), self.input.position)
                _G_apply_1173, lastError = self._apply(self.rule_S, "S", [])
                self.considerError(lastError, None)
                self._trace('  ', (9795, 9797), self.input.position)
                _G_apply_1174, lastError = self._apply(self.rule_E, "E", [])
                self.considerError(lastError, None)
                self._trace('   ', (9797, 9800), self.input.position)
                _G_apply_1175, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('Expression:', (9800, 9811), self.input.position)
                _G_apply_1176, lastError = self._apply(self.rule_Expression, "Expression", [])
                self.considerError(lastError, None)
                return (_G_apply_1176, self.currentError)
            def _G_optional_1177():
                return (None, self.input.nullError())
            _G_or_1178, lastError = self._or([_G_optional_1169, _G_optional_1177])
            self.considerError(lastError, 'CaseExpression')
            _locals['el'] = _G_or_1178
            self._trace('                    ', (9816, 9836), self.input.position)
            _G_apply_1179, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'CaseExpression')
            self._trace('  ', (9836, 9838), self.input.position)
            _G_apply_1180, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'CaseExpression')
            self._trace('  ', (9838, 9840), self.input.position)
            _G_apply_1181, lastError = self._apply(self.rule_N, "N", [])
            self.considerError(lastError, 'CaseExpression')
            self._trace('  ', (9840, 9842), self.input.position)
            _G_apply_1182, lastError = self._apply(self.rule_D, "D", [])
            self.considerError(lastError, 'CaseExpression')
            _G_python_1184, lastError = eval(self._G_expr_1183, self.globals, _locals), None
            self.considerError(lastError, 'CaseExpression')
            return (_G_python_1184, self.currentError)


        def rule_CaseAlternatives(self):
            _locals = {'self': self}
            self.locals['CaseAlternatives'] = _locals
            self._trace('  ', (9904, 9906), self.input.position)
            _G_apply_1185, lastError = self._apply(self.rule_W, "W", [])
            self.considerError(lastError, 'CaseAlternatives')
            self._trace('  ', (9906, 9908), self.input.position)
            _G_apply_1186, lastError = self._apply(self.rule_H, "H", [])
            self.considerError(lastError, 'CaseAlternatives')
            self._trace('  ', (9908, 9910), self.input.position)
            _G_apply_1187, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'CaseAlternatives')
            self._trace('  ', (9910, 9912), self.input.position)
            _G_apply_1188, lastError = self._apply(self.rule_N, "N", [])
            self.considerError(lastError, 'CaseAlternatives')
            self._trace('   ', (9912, 9915), self.input.position)
            _G_apply_1189, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'CaseAlternatives')
            self._trace('         )*', (9915, 9926), self.input.position)
            _G_apply_1190, lastError = self._apply(self.rule_Expression, "Expression", [])
            self.considerError(lastError, 'CaseAlternatives')
            _locals['ex1'] = _G_apply_1190
            self._trace('l -', (9930, 9933), self.input.position)
            _G_apply_1191, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'CaseAlternatives')
            self._trace('> ', (9933, 9935), self.input.position)
            _G_apply_1192, lastError = self._apply(self.rule_T, "T", [])
            self.considerError(lastError, 'CaseAlternatives')
            self._trace('[h', (9935, 9937), self.input.position)
            _G_apply_1193, lastError = self._apply(self.rule_H, "H", [])
            self.considerError(lastError, 'CaseAlternatives')
            self._trace('ea', (9937, 9939), self.input.position)
            _G_apply_1194, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'CaseAlternatives')
            self._trace('d]', (9939, 9941), self.input.position)
            _G_apply_1195, lastError = self._apply(self.rule_N, "N", [])
            self.considerError(lastError, 'CaseAlternatives')
            self._trace(' + ', (9941, 9944), self.input.position)
            _G_apply_1196, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'CaseAlternatives')
            self._trace('tail\n      ', (9944, 9955), self.input.position)
            _G_apply_1197, lastError = self._apply(self.rule_Expression, "Expression", [])
            self.considerError(lastError, 'CaseAlternatives')
            _locals['ex2'] = _G_apply_1197
            _G_python_1199, lastError = eval(self._G_expr_1198, self.globals, _locals), None
            self.considerError(lastError, 'CaseAlternatives')
            return (_G_python_1199, self.currentError)


        def rule_Variable(self):
            _locals = {'self': self}
            self.locals['Variable'] = _locals
            self._trace('             ', (9985, 9998), self.input.position)
            _G_apply_1200, lastError = self._apply(self.rule_SymbolicName, "SymbolicName", [])
            self.considerError(lastError, 'Variable')
            _locals['s'] = _G_apply_1200
            _G_python_1202, lastError = eval(self._G_expr_1201, self.globals, _locals), None
            self.considerError(lastError, 'Variable')
            return (_G_python_1202, self.currentError)


        def rule_StringLiteral(self):
            _locals = {'self': self}
            self.locals['StringLiteral'] = _locals
            def _G_or_1203():
                self._trace(' \')\' -> ["call", f', (10038, 10056), self.input.position)
                _G_exactly_1204, lastError = self.exactly('"')
                self.considerError(lastError, None)
                def _G_many_1205():
                    def _G_or_1206():
                        def _G_not_1207():
                            def _G_or_1208():
                                self._trace(' di', (10060, 10063), self.input.position)
                                _G_exactly_1209, lastError = self.exactly('"')
                                self.considerError(lastError, None)
                                return (_G_exactly_1209, self.currentError)
                            def _G_or_1210():
                                self._trace('tinc', (10064, 10068), self.input.position)
                                _G_exactly_1211, lastError = self.exactly('\\')
                                self.considerError(lastError, None)
                                return (_G_exactly_1211, self.currentError)
                            _G_or_1212, lastError = self._or([_G_or_1208, _G_or_1210])
                            self.considerError(lastError, None)
                            return (_G_or_1212, self.currentError)
                        _G_not_1213, lastError = self._not(_G_not_1207)
                        self.considerError(lastError, None)
                        self._trace(', args]\n\n', (10069, 10078), self.input.position)
                        _G_apply_1214, lastError = self._apply(self.rule_anything, "anything", [])
                        self.considerError(lastError, None)
                        return (_G_apply_1214, self.currentError)
                    def _G_or_1215():
                        self._trace('  FunctionNa', (10080, 10092), self.input.position)
                        _G_apply_1216, lastError = self._apply(self.rule_EscapedChar, "EscapedChar", [])
                        self.considerError(lastError, None)
                        return (_G_apply_1216, self.currentError)
                    _G_or_1217, lastError = self._or([_G_or_1206, _G_or_1215])
                    self.considerError(lastError, None)
                    return (_G_or_1217, self.currentError)
                _G_many_1218, lastError = self.many(_G_many_1205)
                self.considerError(lastError, None)
                _locals['cs'] = _G_many_1218
                self._trace('Symb', (10097, 10101), self.input.position)
                _G_exactly_1219, lastError = self.exactly('"')
                self.considerError(lastError, None)
                _G_python_1221, lastError = eval(self._G_expr_1220, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_1221, self.currentError)
            def _G_or_1222():
                self._trace(" = '", (10132, 10136), self.input.position)
                _G_apply_1223, lastError = self._apply(self.rule_token, "token", ["'"])
                self.considerError(lastError, None)
                def _G_many_1224():
                    def _G_or_1225():
                        def _G_not_1226():
                            def _G_or_1227():
                                self._trace('ilt', (10140, 10143), self.input.position)
                                _G_apply_1228, lastError = self._apply(self.rule_token, "token", ["'"])
                                self.considerError(lastError, None)
                                return (_G_apply_1228, self.currentError)
                            def _G_or_1229():
                                self._trace('rExp', (10144, 10148), self.input.position)
                                _G_exactly_1230, lastError = self.exactly('\\')
                                self.considerError(lastError, None)
                                return (_G_exactly_1230, self.currentError)
                            _G_or_1231, lastError = self._or([_G_or_1227, _G_or_1229])
                            self.considerError(lastError, None)
                            return (_G_or_1231, self.currentError)
                        _G_not_1232, lastError = self._not(_G_not_1226)
                        self.considerError(lastError, None)
                        self._trace('ession:fe', (10149, 10158), self.input.position)
                        _G_apply_1233, lastError = self._apply(self.rule_anything, "anything", [])
                        self.considerError(lastError, None)
                        return (_G_apply_1233, self.currentError)
                    def _G_or_1234():
                        self._trace("(WS '|' Expr", (10160, 10172), self.input.position)
                        _G_apply_1235, lastError = self._apply(self.rule_EscapedChar, "EscapedChar", [])
                        self.considerError(lastError, None)
                        return (_G_apply_1235, self.currentError)
                    _G_or_1236, lastError = self._or([_G_or_1225, _G_or_1234])
                    self.considerError(lastError, None)
                    return (_G_or_1236, self.currentError)
                _G_many_1237, lastError = self.many(_G_many_1224)
                self.considerError(lastError, None)
                _locals['cs'] = _G_many_1237
                self._trace('n)?:', (10177, 10181), self.input.position)
                _G_apply_1238, lastError = self._apply(self.rule_token, "token", ["'"])
                self.considerError(lastError, None)
                _G_python_1239, lastError = eval(self._G_expr_1220, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_1239, self.currentError)
            _G_or_1240, lastError = self._or([_G_or_1203, _G_or_1222])
            self.considerError(lastError, 'StringLiteral')
            _locals['l'] = _G_or_1240
            _G_python_1242, lastError = eval(self._G_expr_1241, self.globals, _locals), None
            self.considerError(lastError, 'StringLiteral')
            return (_G_python_1242, self.currentError)


        def rule_EscapedChar(self):
            _locals = {'self': self}
            self.locals['EscapedChar'] = _locals
            self._trace("S '.'", (10247, 10252), self.input.position)
            _G_exactly_1243, lastError = self.exactly('\\')
            self.considerError(lastError, 'EscapedChar')
            def _G_or_1244():
                self._trace('KeyN', (10266, 10270), self.input.position)
                _G_exactly_1245, lastError = self.exactly('\\')
                self.considerError(lastError, None)
                _G_python_1246, lastError = ('\\'), None
                self.considerError(lastError, None)
                return (_G_python_1246, self.currentError)
            def _G_or_1247():
                self._trace('pert', (10292, 10296), self.input.position)
                _G_apply_1248, lastError = self._apply(self.rule_token, "token", ["'"])
                self.considerError(lastError, None)
                _G_python_1249, lastError = ("'"), None
                self.considerError(lastError, None)
                return (_G_python_1249, self.currentError)
            def _G_or_1250():
                self._trace('yLoo', (10317, 10321), self.input.position)
                _G_exactly_1251, lastError = self.exactly('"')
                self.considerError(lastError, None)
                _G_python_1252, lastError = ('"'), None
                self.considerError(lastError, None)
                return (_G_python_1252, self.currentError)
            def _G_or_1253():
                self._trace('rt', (10342, 10344), self.input.position)
                _G_apply_1254, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                _G_python_1255, lastError = ('\n'), None
                self.considerError(lastError, None)
                return (_G_python_1255, self.currentError)
            def _G_or_1256():
                self._trace('ty', (10366, 10368), self.input.position)
                _G_apply_1257, lastError = self._apply(self.rule_R, "R", [])
                self.considerError(lastError, None)
                _G_python_1258, lastError = ('\r'), None
                self.considerError(lastError, None)
                return (_G_python_1258, self.currentError)
            def _G_or_1259():
                self._trace('xp', (10390, 10392), self.input.position)
                _G_apply_1260, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                _G_python_1261, lastError = ('\t'), None
                self.considerError(lastError, None)
                return (_G_python_1261, self.currentError)
            def _G_or_1262():
                self._trace('    ', (10414, 10418), self.input.position)
                _G_exactly_1263, lastError = self.exactly('_')
                self.considerError(lastError, None)
                _G_python_1264, lastError = ('_'), None
                self.considerError(lastError, None)
                return (_G_python_1264, self.currentError)
            def _G_or_1265():
                self._trace('    ', (10439, 10443), self.input.position)
                _G_exactly_1266, lastError = self.exactly('%')
                self.considerError(lastError, None)
                _G_python_1267, lastError = ('%'), None
                self.considerError(lastError, None)
                return (_G_python_1267, self.currentError)
            _G_or_1268, lastError = self._or([_G_or_1244, _G_or_1247, _G_or_1250, _G_or_1253, _G_or_1256, _G_or_1259, _G_or_1262, _G_or_1265])
            self.considerError(lastError, 'EscapedChar')
            return (_G_or_1268, self.currentError)


        def rule_NumberLiteral(self):
            _locals = {'self': self}
            self.locals['NumberLiteral'] = _locals
            def _G_or_1269():
                self._trace('          (WS CaseAlternativ', (10483, 10511), self.input.position)
                _G_apply_1270, lastError = self._apply(self.rule_DoubleLiteral, "DoubleLiteral", [])
                self.considerError(lastError, None)
                return (_G_apply_1270, self.currentError)
            def _G_or_1271():
                self._trace('               ', (10527, 10542), self.input.position)
                _G_apply_1272, lastError = self._apply(self.rule_IntegerLiteral, "IntegerLiteral", [])
                self.considerError(lastError, None)
                return (_G_apply_1272, self.currentError)
            _G_or_1273, lastError = self._or([_G_or_1269, _G_or_1271])
            self.considerError(lastError, 'NumberLiteral')
            _locals['l'] = _G_or_1273
            _G_python_1274, lastError = eval(self._G_expr_1241, self.globals, _locals), None
            self.considerError(lastError, 'NumberLiteral')
            return (_G_python_1274, self.currentError)


        def rule_MapLiteral(self):
            _locals = {'self': self}
            self.locals['MapLiteral'] = _locals
            self._trace('  WS', (10592, 10596), self.input.position)
            _G_exactly_1275, lastError = self.exactly('{')
            self.considerError(lastError, 'MapLiteral')
            self._trace(' E ', (10596, 10599), self.input.position)
            _G_apply_1276, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'MapLiteral')
            def _G_or_1277():
                self._trace('e", ex, cas, el]\n\n    CaseAlternativ', (10632, 10668), self.input.position)
                _G_apply_1278, lastError = self._apply(self.rule_PropertyKeyName, "PropertyKeyName", [])
                self.considerError(lastError, None)
                _locals['k'] = _G_apply_1278
                self._trace(' = ', (10670, 10673), self.input.position)
                _G_apply_1279, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('W H ', (10673, 10677), self.input.position)
                _G_exactly_1280, lastError = self.exactly(':')
                self.considerError(lastError, None)
                self._trace('E N', (10677, 10680), self.input.position)
                _G_apply_1281, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace(' WS Express', (10680, 10691), self.input.position)
                _G_apply_1282, lastError = self._apply(self.rule_Expression, "Expression", [])
                self.considerError(lastError, None)
                _locals['v'] = _G_apply_1282
                _G_python_1284, lastError = eval(self._G_expr_1283, self.globals, _locals), None
                self.considerError(lastError, None)
                _locals['head'] = _G_python_1284
                self._trace('2 -', (10726, 10729), self.input.position)
                _G_apply_1285, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                def _G_many_1286():
                    self._trace('Variable = SymbolicName:', (10747, 10771), self.input.position)
                    _G_exactly_1287, lastError = self.exactly(',')
                    self.considerError(lastError, None)
                    self._trace('s -', (10771, 10774), self.input.position)
                    _G_apply_1288, lastError = self._apply(self.rule_WS, "WS", [])
                    self.considerError(lastError, None)
                    self._trace('> ["Variable", s', (10774, 10790), self.input.position)
                    _G_apply_1289, lastError = self._apply(self.rule_PropertyKeyName, "PropertyKeyName", [])
                    self.considerError(lastError, None)
                    _locals['k'] = _G_apply_1289
                    self._trace('\n  ', (10792, 10795), self.input.position)
                    _G_apply_1290, lastError = self._apply(self.rule_WS, "WS", [])
                    self.considerError(lastError, None)
                    self._trace('  St', (10795, 10799), self.input.position)
                    _G_exactly_1291, lastError = self.exactly(':')
                    self.considerError(lastError, None)
                    self._trace('rin', (10799, 10802), self.input.position)
                    _G_apply_1292, lastError = self._apply(self.rule_WS, "WS", [])
                    self.considerError(lastError, None)
                    self._trace('gLiteral = ', (10802, 10813), self.input.position)
                    _G_apply_1293, lastError = self._apply(self.rule_Expression, "Expression", [])
                    self.considerError(lastError, None)
                    _locals['v'] = _G_apply_1293
                    self._trace('   ', (10815, 10818), self.input.position)
                    _G_apply_1294, lastError = self._apply(self.rule_WS, "WS", [])
                    self.considerError(lastError, None)
                    _G_python_1295, lastError = eval(self._G_expr_1283, self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_1295, self.currentError)
                _G_many_1296, lastError = self.many(_G_many_1286)
                self.considerError(lastError, None)
                _locals['tail'] = _G_many_1296
                _G_python_1297, lastError = eval(self._G_expr_442, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_1297, self.currentError)
            def _G_or_1298():
                _G_python_1299, lastError = ([]), None
                self.considerError(lastError, None)
                return (_G_python_1299, self.currentError)
            _G_or_1300, lastError = self._or([_G_or_1277, _G_or_1298])
            self.considerError(lastError, 'MapLiteral')
            _locals['pairs'] = _G_or_1300
            self._trace('                ', (10897, 10913), self.input.position)
            _G_exactly_1301, lastError = self.exactly('}')
            self.considerError(lastError, 'MapLiteral')
            _G_python_1303, lastError = eval(self._G_expr_1302, self.globals, _locals), None
            self.considerError(lastError, 'MapLiteral')
            return (_G_python_1303, self.currentError)


        def rule_Parameter(self):
            _locals = {'self': self}
            self.locals['Parameter'] = _locals
            self._trace('ar)*', (10954, 10958), self.input.position)
            _G_exactly_1304, lastError = self.exactly('$')
            self.considerError(lastError, 'Parameter')
            def _G_or_1305():
                self._trace('s "\'" -> "".', (10960, 10972), self.input.position)
                _G_apply_1306, lastError = self._apply(self.rule_SymbolicName, "SymbolicName", [])
                self.considerError(lastError, None)
                return (_G_apply_1306, self.currentError)
            def _G_or_1307():
                self._trace('in(cs)\n        ', (10974, 10989), self.input.position)
                _G_apply_1308, lastError = self._apply(self.rule_DecimalInteger, "DecimalInteger", [])
                self.considerError(lastError, None)
                return (_G_apply_1308, self.currentError)
            _G_or_1309, lastError = self._or([_G_or_1305, _G_or_1307])
            self.considerError(lastError, 'Parameter')
            _locals['p'] = _G_or_1309
            _G_python_1311, lastError = eval(self._G_expr_1310, self.globals, _locals), None
            self.considerError(lastError, 'Parameter')
            return (_G_python_1311, self.currentError)


        def rule_PropertyExpression(self):
            _locals = {'self': self}
            self.locals['PropertyExpression'] = _locals
            self._trace('har =', (11034, 11039), self.input.position)
            _G_apply_1312, lastError = self._apply(self.rule_Atom, "Atom", [])
            self.considerError(lastError, 'PropertyExpression')
            _locals['a'] = _G_apply_1312
            def _G_many_1313():
                self._trace("'\n", (11043, 11045), self.input.position)
                _G_apply_1314, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('               ', (11045, 11060), self.input.position)
                _G_apply_1315, lastError = self._apply(self.rule_PropertyLookup, "PropertyLookup", [])
                self.considerError(lastError, None)
                return (_G_apply_1315, self.currentError)
            _G_many_1316, lastError = self.many(_G_many_1313)
            self.considerError(lastError, 'PropertyExpression')
            _locals['opts'] = _G_many_1316
            _G_python_1318, lastError = eval(self._G_expr_1317, self.globals, _locals), None
            self.considerError(lastError, 'PropertyExpression')
            return (_G_python_1318, self.currentError)


        def rule_PropertyKeyName(self):
            _locals = {'self': self}
            self.locals['PropertyKeyName'] = _locals
            self._trace('       | \'"\' ', (11113, 11126), self.input.position)
            _G_apply_1319, lastError = self._apply(self.rule_SymbolicName, "SymbolicName", [])
            self.considerError(lastError, 'PropertyKeyName')
            return (_G_apply_1319, self.currentError)


        def rule_IntegerLiteral(self):
            _locals = {'self': self}
            self.locals['IntegerLiteral'] = _locals
            def _G_or_1320():
                self._trace('     | N ->', (11144, 11155), self.input.position)
                _G_apply_1321, lastError = self._apply(self.rule_HexInteger, "HexInteger", [])
                self.considerError(lastError, None)
                return (_G_apply_1321, self.currentError)
            def _G_or_1322():
                self._trace("     | R -> '", (11172, 11185), self.input.position)
                _G_apply_1323, lastError = self._apply(self.rule_OctalInteger, "OctalInteger", [])
                self.considerError(lastError, None)
                return (_G_apply_1323, self.currentError)
            def _G_or_1324():
                self._trace("   | T -> '\\t'\n", (11202, 11217), self.input.position)
                _G_apply_1325, lastError = self._apply(self.rule_DecimalInteger, "DecimalInteger", [])
                self.considerError(lastError, None)
                return (_G_apply_1325, self.currentError)
            _G_or_1326, lastError = self._or([_G_or_1320, _G_or_1322, _G_or_1324])
            self.considerError(lastError, 'IntegerLiteral')
            return (_G_or_1326, self.currentError)


        def rule_OctalDigit(self):
            _locals = {'self': self}
            self.locals['OctalDigit'] = _locals
            def _G_not_1327():
                def _G_or_1328():
                    self._trace(" '_", (11234, 11237), self.input.position)
                    _G_exactly_1329, lastError = self.exactly('8')
                    self.considerError(lastError, None)
                    return (_G_exactly_1329, self.currentError)
                def _G_or_1330():
                    self._trace(' ->', (11238, 11241), self.input.position)
                    _G_exactly_1331, lastError = self.exactly('9')
                    self.considerError(lastError, None)
                    return (_G_exactly_1331, self.currentError)
                _G_or_1332, lastError = self._or([_G_or_1328, _G_or_1330])
                self.considerError(lastError, None)
                return (_G_or_1332, self.currentError)
            _G_not_1333, lastError = self._not(_G_not_1327)
            self.considerError(lastError, 'OctalDigit')
            self._trace("'_'\n  ", (11242, 11248), self.input.position)
            _G_apply_1334, lastError = self._apply(self.rule_digit, "digit", [])
            self.considerError(lastError, 'OctalDigit')
            return (_G_apply_1334, self.currentError)


        def rule_OctalInteger(self):
            _locals = {'self': self}
            self.locals['OctalInteger'] = _locals
            self._trace("'%' ", (11264, 11268), self.input.position)
            _G_exactly_1335, lastError = self.exactly('0')
            self.considerError(lastError, 'OctalInteger')
            def _G_consumedby_1336():
                def _G_many1_1337():
                    self._trace(" '%'\n     ", (11270, 11280), self.input.position)
                    _G_apply_1338, lastError = self._apply(self.rule_OctalDigit, "OctalDigit", [])
                    self.considerError(lastError, None)
                    return (_G_apply_1338, self.currentError)
                _G_many1_1339, lastError = self.many(_G_many1_1337, _G_many1_1337())
                self.considerError(lastError, None)
                return (_G_many1_1339, self.currentError)
            _G_consumedby_1340, lastError = self.consumedby(_G_consumedby_1336)
            self.considerError(lastError, 'OctalInteger')
            _locals['ds'] = _G_consumedby_1340
            _G_python_1342, lastError = eval(self._G_expr_1341, self.globals, _locals), None
            self.considerError(lastError, 'OctalInteger')
            return (_G_python_1342, self.currentError)


        def rule_HexDigit(self):
            _locals = {'self': self}
            self.locals['HexDigit'] = _locals
            def _G_or_1343():
                self._trace(' = (\n ', (11311, 11317), self.input.position)
                _G_apply_1344, lastError = self._apply(self.rule_digit, "digit", [])
                self.considerError(lastError, None)
                return (_G_apply_1344, self.currentError)
            def _G_or_1345():
                self._trace('  ', (11319, 11321), self.input.position)
                _G_apply_1346, lastError = self._apply(self.rule_A, "A", [])
                self.considerError(lastError, None)
                return (_G_apply_1346, self.currentError)
            def _G_or_1347():
                self._trace('  ', (11323, 11325), self.input.position)
                _G_apply_1348, lastError = self._apply(self.rule_B, "B", [])
                self.considerError(lastError, None)
                return (_G_apply_1348, self.currentError)
            def _G_or_1349():
                self._trace('  ', (11327, 11329), self.input.position)
                _G_apply_1350, lastError = self._apply(self.rule_C, "C", [])
                self.considerError(lastError, None)
                return (_G_apply_1350, self.currentError)
            def _G_or_1351():
                self._trace('  ', (11331, 11333), self.input.position)
                _G_apply_1352, lastError = self._apply(self.rule_D, "D", [])
                self.considerError(lastError, None)
                return (_G_apply_1352, self.currentError)
            def _G_or_1353():
                self._trace('ou', (11335, 11337), self.input.position)
                _G_apply_1354, lastError = self._apply(self.rule_E, "E", [])
                self.considerError(lastError, None)
                return (_G_apply_1354, self.currentError)
            def _G_or_1355():
                self._trace('eL', (11339, 11341), self.input.position)
                _G_apply_1356, lastError = self._apply(self.rule_F, "F", [])
                self.considerError(lastError, None)
                return (_G_apply_1356, self.currentError)
            _G_or_1357, lastError = self._or([_G_or_1343, _G_or_1345, _G_or_1347, _G_or_1349, _G_or_1351, _G_or_1353, _G_or_1355])
            self.considerError(lastError, 'HexDigit')
            return (_G_or_1357, self.currentError)


        def rule_HexInteger(self):
            _locals = {'self': self}
            self.locals['HexInteger'] = _locals
            self._trace('    ', (11355, 11359), self.input.position)
            _G_exactly_1358, lastError = self.exactly('0')
            self.considerError(lastError, 'HexInteger')
            self._trace('  ', (11359, 11361), self.input.position)
            _G_apply_1359, lastError = self._apply(self.rule_X, "X", [])
            self.considerError(lastError, 'HexInteger')
            def _G_consumedby_1360():
                def _G_many1_1361():
                    self._trace('   | Int', (11363, 11371), self.input.position)
                    _G_apply_1362, lastError = self._apply(self.rule_HexDigit, "HexDigit", [])
                    self.considerError(lastError, None)
                    return (_G_apply_1362, self.currentError)
                _G_many1_1363, lastError = self.many(_G_many1_1361, _G_many1_1361())
                self.considerError(lastError, None)
                return (_G_many1_1363, self.currentError)
            _G_consumedby_1364, lastError = self.consumedby(_G_consumedby_1360)
            self.considerError(lastError, 'HexInteger')
            _locals['ds'] = _G_consumedby_1364
            _G_python_1366, lastError = eval(self._G_expr_1365, self.globals, _locals), None
            self.considerError(lastError, 'HexInteger')
            return (_G_python_1366, self.currentError)


        def rule_DecimalInteger(self):
            _locals = {'self': self}
            self.locals['DecimalInteger'] = _locals
            def _G_consumedby_1367():
                def _G_many1_1368():
                    self._trace('itera', (11411, 11416), self.input.position)
                    _G_apply_1369, lastError = self._apply(self.rule_digit, "digit", [])
                    self.considerError(lastError, None)
                    return (_G_apply_1369, self.currentError)
                _G_many1_1370, lastError = self.many(_G_many1_1368, _G_many1_1368())
                self.considerError(lastError, None)
                return (_G_many1_1370, self.currentError)
            _G_consumedby_1371, lastError = self.consumedby(_G_consumedby_1367)
            self.considerError(lastError, 'DecimalInteger')
            _locals['ds'] = _G_consumedby_1371
            _G_python_1373, lastError = eval(self._G_expr_1372, self.globals, _locals), None
            self.considerError(lastError, 'DecimalInteger')
            return (_G_python_1373, self.currentError)


        def rule_DoubleLiteral(self):
            _locals = {'self': self}
            self.locals['DoubleLiteral'] = _locals
            def _G_or_1374():
                self._trace('                (\n  ', (11449, 11469), self.input.position)
                _G_apply_1375, lastError = self._apply(self.rule_ExponentDecimalReal, "ExponentDecimalReal", [])
                self.considerError(lastError, None)
                return (_G_apply_1375, self.currentError)
            def _G_or_1376():
                self._trace('  (\n               ', (11485, 11504), self.input.position)
                _G_apply_1377, lastError = self._apply(self.rule_RegularDecimalReal, "RegularDecimalReal", [])
                self.considerError(lastError, None)
                return (_G_apply_1377, self.currentError)
            _G_or_1378, lastError = self._or([_G_or_1374, _G_or_1376])
            self.considerError(lastError, 'DoubleLiteral')
            return (_G_or_1378, self.currentError)


        def rule_ExponentDecimalReal(self):
            _locals = {'self': self}
            self.locals['ExponentDecimalReal'] = _locals
            def _G_consumedby_1379():
                def _G_or_1380():
                    self._trace(" WS ':' WS Express", (11530, 11548), self.input.position)
                    _G_apply_1381, lastError = self._apply(self.rule_RegularDecimalReal, "RegularDecimalReal", [])
                    self.considerError(lastError, None)
                    return (_G_apply_1381, self.currentError)
                def _G_or_1382():
                    self._trace('n:v -> (k, v)\n ', (11550, 11565), self.input.position)
                    _G_apply_1383, lastError = self._apply(self.rule_DecimalInteger, "DecimalInteger", [])
                    self.considerError(lastError, None)
                    return (_G_apply_1383, self.currentError)
                _G_or_1384, lastError = self._or([_G_or_1380, _G_or_1382])
                self.considerError(lastError, None)
                self._trace('  ', (11566, 11568), self.input.position)
                _G_apply_1385, lastError = self._apply(self.rule_E, "E", [])
                self.considerError(lastError, None)
                def _G_optional_1386():
                    def _G_or_1387():
                        self._trace('   ', (11570, 11573), self.input.position)
                        _G_exactly_1388, lastError = self.exactly('+')
                        self.considerError(lastError, None)
                        return (_G_exactly_1388, self.currentError)
                    def _G_or_1389():
                        self._trace('    ', (11575, 11579), self.input.position)
                        _G_exactly_1390, lastError = self.exactly('-')
                        self.considerError(lastError, None)
                        return (_G_exactly_1390, self.currentError)
                    _G_or_1391, lastError = self._or([_G_or_1387, _G_or_1389])
                    self.considerError(lastError, None)
                    return (_G_or_1391, self.currentError)
                def _G_optional_1392():
                    return (None, self.input.nullError())
                _G_or_1393, lastError = self._or([_G_optional_1386, _G_optional_1392])
                self.considerError(lastError, None)
                self._trace('   ):head WS\n  ', (11581, 11596), self.input.position)
                _G_apply_1394, lastError = self._apply(self.rule_DecimalInteger, "DecimalInteger", [])
                self.considerError(lastError, None)
                return (_G_apply_1394, self.currentError)
            _G_consumedby_1395, lastError = self.consumedby(_G_consumedby_1379)
            self.considerError(lastError, 'ExponentDecimalReal')
            _locals['ds'] = _G_consumedby_1395
            _G_python_1397, lastError = eval(self._G_expr_1396, self.globals, _locals), None
            self.considerError(lastError, 'ExponentDecimalReal')
            return (_G_python_1397, self.currentError)


        def rule_RegularDecimalReal(self):
            _locals = {'self': self}
            self.locals['RegularDecimalReal'] = _locals
            def _G_or_1398():
                def _G_consumedby_1399():
                    def _G_many1_1400():
                        self._trace("  ','", (11638, 11643), self.input.position)
                        _G_apply_1401, lastError = self._apply(self.rule_digit, "digit", [])
                        self.considerError(lastError, None)
                        return (_G_apply_1401, self.currentError)
                    _G_many1_1402, lastError = self.many(_G_many1_1400, _G_many1_1400())
                    self.considerError(lastError, None)
                    self._trace('WS P', (11644, 11648), self.input.position)
                    _G_exactly_1403, lastError = self.exactly('.')
                    self.considerError(lastError, None)
                    def _G_many1_1404():
                        self._trace('ropert', (11648, 11654), self.input.position)
                        _G_apply_1405, lastError = self._apply(self.rule_digit, "digit", [])
                        self.considerError(lastError, None)
                        return (_G_apply_1405, self.currentError)
                    _G_many1_1406, lastError = self.many(_G_many1_1404, _G_many1_1404())
                    self.considerError(lastError, None)
                    return (_G_many1_1406, self.currentError)
                _G_consumedby_1407, lastError = self.consumedby(_G_consumedby_1399)
                self.considerError(lastError, None)
                return (_G_consumedby_1407, self.currentError)
            def _G_or_1408():
                def _G_consumedby_1409():
                    def _G_many1_1410():
                        self._trace('me:k ', (11660, 11665), self.input.position)
                        _G_apply_1411, lastError = self._apply(self.rule_digit, "digit", [])
                        self.considerError(lastError, None)
                        return (_G_apply_1411, self.currentError)
                    _G_many1_1412, lastError = self.many(_G_many1_1410, _G_many1_1410())
                    self.considerError(lastError, None)
                    self._trace("S ':", (11666, 11670), self.input.position)
                    _G_exactly_1413, lastError = self.exactly('.')
                    self.considerError(lastError, None)
                    return (_G_exactly_1413, self.currentError)
                _G_consumedby_1414, lastError = self.consumedby(_G_consumedby_1409)
                self.considerError(lastError, None)
                return (_G_consumedby_1414, self.currentError)
            def _G_or_1415():
                def _G_consumedby_1416():
                    self._trace('Exp', (11675, 11678), self.input.position)
                    _G_exactly_1417, lastError = self.exactly('.')
                    self.considerError(lastError, None)
                    def _G_many1_1418():
                        self._trace('ressio', (11678, 11684), self.input.position)
                        _G_apply_1419, lastError = self._apply(self.rule_digit, "digit", [])
                        self.considerError(lastError, None)
                        return (_G_apply_1419, self.currentError)
                    _G_many1_1420, lastError = self.many(_G_many1_1418, _G_many1_1418())
                    self.considerError(lastError, None)
                    return (_G_many1_1420, self.currentError)
                _G_consumedby_1421, lastError = self.consumedby(_G_consumedby_1416)
                self.considerError(lastError, None)
                return (_G_consumedby_1421, self.currentError)
            _G_or_1422, lastError = self._or([_G_or_1398, _G_or_1408, _G_or_1415])
            self.considerError(lastError, 'RegularDecimalReal')
            _locals['ds'] = _G_or_1422
            _G_python_1423, lastError = eval(self._G_expr_1396, self.globals, _locals), None
            self.considerError(lastError, 'RegularDecimalReal')
            return (_G_python_1423, self.currentError)


        def rule_SymbolicName(self):
            _locals = {'self': self}
            self.locals['SymbolicName'] = _locals
            def _G_or_1424():
                self._trace('  )*:tail -> [head] + ', (11719, 11741), self.input.position)
                _G_apply_1425, lastError = self._apply(self.rule_UnescapedSymbolicName, "UnescapedSymbolicName", [])
                self.considerError(lastError, None)
                return (_G_apply_1425, self.currentError)
            def _G_or_1426():
                self._trace('       | -> []):pair', (11756, 11776), self.input.position)
                _G_apply_1427, lastError = self._apply(self.rule_EscapedSymbolicName, "EscapedSymbolicName", [])
                self.considerError(lastError, None)
                return (_G_apply_1427, self.currentError)
            _G_or_1428, lastError = self._or([_G_or_1424, _G_or_1426])
            self.considerError(lastError, 'SymbolicName')
            return (_G_or_1428, self.currentError)


        def rule_UnescapedSymbolicName(self):
            _locals = {'self': self}
            self.locals['UnescapedSymbolicName'] = _locals
            def _G_consumedby_1429():
                self._trace('Litera', (11803, 11809), self.input.position)
                _G_apply_1430, lastError = self._apply(self.rule_letter, "letter", [])
                self.considerError(lastError, None)
                def _G_many_1431():
                    def _G_or_1432():
                        self._trace(', d', (11811, 11814), self.input.position)
                        _G_exactly_1433, lastError = self.exactly('_')
                        self.considerError(lastError, None)
                        return (_G_exactly_1433, self.currentError)
                    def _G_or_1434():
                        self._trace('t(pairs)]\n\n   ', (11816, 11830), self.input.position)
                        _G_apply_1435, lastError = self._apply(self.rule_letterOrDigit, "letterOrDigit", [])
                        self.considerError(lastError, None)
                        return (_G_apply_1435, self.currentError)
                    _G_or_1436, lastError = self._or([_G_or_1432, _G_or_1434])
                    self.considerError(lastError, None)
                    return (_G_or_1436, self.currentError)
                _G_many_1437, lastError = self.many(_G_many_1431)
                self.considerError(lastError, None)
                return (_G_many_1437, self.currentError)
            _G_consumedby_1438, lastError = self.consumedby(_G_consumedby_1429)
            self.considerError(lastError, 'UnescapedSymbolicName')
            return (_G_consumedby_1438, self.currentError)


        def rule_EscapedSymbolicName(self):
            _locals = {'self': self}
            self.locals['EscapedSymbolicName'] = _locals
            self._trace('Name', (11856, 11860), self.input.position)
            _G_exactly_1439, lastError = self.exactly('`')
            self.considerError(lastError, 'EscapedSymbolicName')
            def _G_many_1440():
                def _G_or_1441():
                    def _G_not_1442():
                        self._trace('Dec', (11863, 11866), self.input.position)
                        _G_exactly_1443, lastError = self.exactly('`')
                        self.considerError(lastError, None)
                        return (_G_exactly_1443, self.currentError)
                    _G_not_1444, lastError = self._not(_G_not_1442)
                    self.considerError(lastError, None)
                    self._trace('imalInteg', (11866, 11875), self.input.position)
                    _G_apply_1445, lastError = self._apply(self.rule_anything, "anything", [])
                    self.considerError(lastError, None)
                    return (_G_apply_1445, self.currentError)
                def _G_or_1446():
                    self._trace('):p -', (11877, 11882), self.input.position)
                    _G_apply_1447, lastError = self._apply(self.rule_token, "token", ["``"])
                    self.considerError(lastError, None)
                    _G_python_1448, lastError = ('`'), None
                    self.considerError(lastError, None)
                    return (_G_python_1448, self.currentError)
                _G_or_1449, lastError = self._or([_G_or_1441, _G_or_1446])
                self.considerError(lastError, None)
                return (_G_or_1449, self.currentError)
            _G_many_1450, lastError = self.many(_G_many_1440)
            self.considerError(lastError, 'EscapedSymbolicName')
            _locals['cs'] = _G_many_1450
            self._trace('r", ', (11894, 11898), self.input.position)
            _G_exactly_1451, lastError = self.exactly('`')
            self.considerError(lastError, 'EscapedSymbolicName')
            _G_python_1452, lastError = eval(self._G_expr_1220, self.globals, _locals), None
            self.considerError(lastError, 'EscapedSymbolicName')
            return (_G_python_1452, self.currentError)


        def rule_WS(self):
            _locals = {'self': self}
            self.locals['WS'] = _locals
            def _G_many_1453():
                self._trace('ssion = Ato', (11919, 11930), self.input.position)
                _G_apply_1454, lastError = self._apply(self.rule_whitespace, "whitespace", [])
                self.considerError(lastError, None)
                return (_G_apply_1454, self.currentError)
            _G_many_1455, lastError = self.many(_G_many_1453)
            self.considerError(lastError, 'WS')
            return (_G_many_1455, self.currentError)


        def rule_SP(self):
            _locals = {'self': self}
            self.locals['SP'] = _locals
            def _G_many1_1456():
                self._trace(' PropertyLo', (11937, 11948), self.input.position)
                _G_apply_1457, lastError = self._apply(self.rule_whitespace, "whitespace", [])
                self.considerError(lastError, None)
                return (_G_apply_1457, self.currentError)
            _G_many1_1458, lastError = self.many(_G_many1_1456, _G_many1_1456())
            self.considerError(lastError, 'SP')
            return (_G_many1_1458, self.currentError)


        def rule_whitespace(self):
            _locals = {'self': self}
            self.locals['whitespace'] = _locals
            def _G_or_1459():
                self._trace('["Ex', (11963, 11967), self.input.position)
                _G_exactly_1460, lastError = self.exactly(' ')
                self.considerError(lastError, None)
                return (_G_exactly_1460, self.currentError)
            def _G_or_1461():
                self._trace(' opts', (11980, 11985), self.input.position)
                _G_exactly_1462, lastError = self.exactly('\t')
                self.considerError(lastError, None)
                return (_G_exactly_1462, self.currentError)
            def _G_or_1463():
                self._trace('tyKey', (11998, 12003), self.input.position)
                _G_exactly_1464, lastError = self.exactly('\n')
                self.considerError(lastError, None)
                return (_G_exactly_1464, self.currentError)
            def _G_or_1465():
                self._trace('icName\n\n', (12016, 12024), self.input.position)
                _G_apply_1466, lastError = self._apply(self.rule_Comment, "Comment", [])
                self.considerError(lastError, None)
                return (_G_apply_1466, self.currentError)
            _G_or_1467, lastError = self._or([_G_or_1459, _G_or_1461, _G_or_1463, _G_or_1465])
            self.considerError(lastError, 'whitespace')
            return (_G_or_1467, self.currentError)


        def rule_Comment(self):
            _locals = {'self': self}
            self.locals['Comment'] = _locals
            def _G_or_1468():
                self._trace('Liter', (12035, 12040), self.input.position)
                _G_apply_1469, lastError = self._apply(self.rule_token, "token", ["/*"])
                self.considerError(lastError, None)
                def _G_many_1470():
                    def _G_not_1471():
                        self._trace('= He', (12043, 12047), self.input.position)
                        _G_apply_1472, lastError = self._apply(self.rule_token, "token", ["*/"])
                        self.considerError(lastError, None)
                        return (_G_apply_1472, self.currentError)
                    _G_not_1473, lastError = self._not(_G_not_1471)
                    self.considerError(lastError, None)
                    self._trace('xInteger\n', (12047, 12056), self.input.position)
                    _G_apply_1474, lastError = self._apply(self.rule_anything, "anything", [])
                    self.considerError(lastError, None)
                    return (_G_apply_1474, self.currentError)
                _G_many_1475, lastError = self.many(_G_many_1470)
                self.considerError(lastError, None)
                self._trace('     ', (12058, 12063), self.input.position)
                _G_apply_1476, lastError = self._apply(self.rule_token, "token", ["*/"])
                self.considerError(lastError, None)
                return (_G_apply_1476, self.currentError)
            def _G_or_1477():
                self._trace('  | O', (12073, 12078), self.input.position)
                _G_apply_1478, lastError = self._apply(self.rule_token, "token", ["//"])
                self.considerError(lastError, None)
                def _G_many_1479():
                    def _G_not_1480():
                        def _G_or_1481():
                            self._trace('Inte', (12082, 12086), self.input.position)
                            _G_exactly_1482, lastError = self.exactly('\r')
                            self.considerError(lastError, None)
                            return (_G_exactly_1482, self.currentError)
                        def _G_or_1483():
                            self._trace('er\n ', (12087, 12091), self.input.position)
                            _G_exactly_1484, lastError = self.exactly('\n')
                            self.considerError(lastError, None)
                            return (_G_exactly_1484, self.currentError)
                        _G_or_1485, lastError = self._or([_G_or_1481, _G_or_1483])
                        self.considerError(lastError, None)
                        return (_G_or_1485, self.currentError)
                    _G_not_1486, lastError = self._not(_G_not_1480)
                    self.considerError(lastError, None)
                    self._trace('         ', (12092, 12101), self.input.position)
                    _G_apply_1487, lastError = self._apply(self.rule_anything, "anything", [])
                    self.considerError(lastError, None)
                    return (_G_apply_1487, self.currentError)
                _G_many_1488, lastError = self.many(_G_many_1479)
                self.considerError(lastError, None)
                def _G_optional_1489():
                    self._trace('     ', (12103, 12108), self.input.position)
                    _G_exactly_1490, lastError = self.exactly('\r')
                    self.considerError(lastError, None)
                    return (_G_exactly_1490, self.currentError)
                def _G_optional_1491():
                    return (None, self.input.nullError())
                _G_or_1492, lastError = self._or([_G_optional_1489, _G_optional_1491])
                self.considerError(lastError, None)
                def _G_or_1493():
                    self._trace('Deci', (12111, 12115), self.input.position)
                    _G_exactly_1494, lastError = self.exactly('\n')
                    self.considerError(lastError, None)
                    return (_G_exactly_1494, self.currentError)
                def _G_or_1495():
                    self._trace('alI', (12116, 12119), self.input.position)
                    _G_apply_1496, lastError = self._apply(self.rule_end, "end", [])
                    self.considerError(lastError, None)
                    return (_G_apply_1496, self.currentError)
                _G_or_1497, lastError = self._or([_G_or_1493, _G_or_1495])
                self.considerError(lastError, None)
                return (_G_or_1497, self.currentError)
            _G_or_1498, lastError = self._or([_G_or_1468, _G_or_1477])
            self.considerError(lastError, 'Comment')
            return (_G_or_1498, self.currentError)


        def rule_LeftArrowHead(self):
            _locals = {'self': self}
            self.locals['LeftArrowHead'] = _locals
            self._trace('igit', (12137, 12141), self.input.position)
            _G_exactly_1499, lastError = self.exactly('<')
            self.considerError(lastError, 'LeftArrowHead')
            return (_G_exactly_1499, self.currentError)


        def rule_RightArrowHead(self):
            _locals = {'self': self}
            self.locals['RightArrowHead'] = _locals
            self._trace('t\n\n ', (12159, 12163), self.input.position)
            _G_exactly_1500, lastError = self.exactly('>')
            self.considerError(lastError, 'RightArrowHead')
            return (_G_exactly_1500, self.currentError)


        def rule_Dash(self):
            _locals = {'self': self}
            self.locals['Dash'] = _locals
            self._trace('Inte', (12171, 12175), self.input.position)
            _G_exactly_1501, lastError = self.exactly('-')
            self.considerError(lastError, 'Dash')
            return (_G_exactly_1501, self.currentError)


        def rule_A(self):
            _locals = {'self': self}
            self.locals['A'] = _locals
            def _G_or_1502():
                self._trace(" '0'", (12180, 12184), self.input.position)
                _G_exactly_1503, lastError = self.exactly('A')
                self.considerError(lastError, None)
                return (_G_exactly_1503, self.currentError)
            def _G_or_1504():
                self._trace('Octa', (12186, 12190), self.input.position)
                _G_exactly_1505, lastError = self.exactly('a')
                self.considerError(lastError, None)
                return (_G_exactly_1505, self.currentError)
            _G_or_1506, lastError = self._or([_G_or_1502, _G_or_1504])
            self.considerError(lastError, 'A')
            return (_G_or_1506, self.currentError)


        def rule_B(self):
            _locals = {'self': self}
            self.locals['B'] = _locals
            def _G_or_1507():
                self._trace('t+>:', (12195, 12199), self.input.position)
                _G_exactly_1508, lastError = self.exactly('B')
                self.considerError(lastError, None)
                return (_G_exactly_1508, self.currentError)
            def _G_or_1509():
                self._trace(' -> ', (12201, 12205), self.input.position)
                _G_exactly_1510, lastError = self.exactly('b')
                self.considerError(lastError, None)
                return (_G_exactly_1510, self.currentError)
            _G_or_1511, lastError = self._or([_G_or_1507, _G_or_1509])
            self.considerError(lastError, 'B')
            return (_G_or_1511, self.currentError)


        def rule_C(self):
            _locals = {'self': self}
            self.locals['C'] = _locals
            def _G_or_1512():
                self._trace('s, 8', (12210, 12214), self.input.position)
                _G_exactly_1513, lastError = self.exactly('C')
                self.considerError(lastError, None)
                return (_G_exactly_1513, self.currentError)
            def _G_or_1514():
                self._trace('\n   ', (12216, 12220), self.input.position)
                _G_exactly_1515, lastError = self.exactly('c')
                self.considerError(lastError, None)
                return (_G_exactly_1515, self.currentError)
            _G_or_1516, lastError = self._or([_G_or_1512, _G_or_1514])
            self.considerError(lastError, 'C')
            return (_G_or_1516, self.currentError)


        def rule_D(self):
            _locals = {'self': self}
            self.locals['D'] = _locals
            def _G_or_1517():
                self._trace('igit', (12225, 12229), self.input.position)
                _G_exactly_1518, lastError = self.exactly('D')
                self.considerError(lastError, None)
                return (_G_exactly_1518, self.currentError)
            def _G_or_1519():
                self._trace(' dig', (12231, 12235), self.input.position)
                _G_exactly_1520, lastError = self.exactly('d')
                self.considerError(lastError, None)
                return (_G_exactly_1520, self.currentError)
            _G_or_1521, lastError = self._or([_G_or_1517, _G_or_1519])
            self.considerError(lastError, 'D')
            return (_G_or_1521, self.currentError)


        def rule_E(self):
            _locals = {'self': self}
            self.locals['E'] = _locals
            def _G_or_1522():
                self._trace('A | ', (12240, 12244), self.input.position)
                _G_exactly_1523, lastError = self.exactly('E')
                self.considerError(lastError, None)
                return (_G_exactly_1523, self.currentError)
            def _G_or_1524():
                self._trace('| C ', (12246, 12250), self.input.position)
                _G_exactly_1525, lastError = self.exactly('e')
                self.considerError(lastError, None)
                return (_G_exactly_1525, self.currentError)
            _G_or_1526, lastError = self._or([_G_or_1522, _G_or_1524])
            self.considerError(lastError, 'E')
            return (_G_or_1526, self.currentError)


        def rule_F(self):
            _locals = {'self': self}
            self.locals['F'] = _locals
            def _G_or_1527():
                self._trace(' E |', (12255, 12259), self.input.position)
                _G_exactly_1528, lastError = self.exactly('F')
                self.considerError(lastError, None)
                return (_G_exactly_1528, self.currentError)
            def _G_or_1529():
                self._trace('\n\n  ', (12261, 12265), self.input.position)
                _G_exactly_1530, lastError = self.exactly('f')
                self.considerError(lastError, None)
                return (_G_exactly_1530, self.currentError)
            _G_or_1531, lastError = self._or([_G_or_1527, _G_or_1529])
            self.considerError(lastError, 'F')
            return (_G_or_1531, self.currentError)


        def rule_G(self):
            _locals = {'self': self}
            self.locals['G'] = _locals
            def _G_or_1532():
                self._trace('Inte', (12270, 12274), self.input.position)
                _G_exactly_1533, lastError = self.exactly('G')
                self.considerError(lastError, None)
                return (_G_exactly_1533, self.currentError)
            def _G_or_1534():
                self._trace('r = ', (12276, 12280), self.input.position)
                _G_exactly_1535, lastError = self.exactly('g')
                self.considerError(lastError, None)
                return (_G_exactly_1535, self.currentError)
            _G_or_1536, lastError = self._or([_G_or_1532, _G_or_1534])
            self.considerError(lastError, 'G')
            return (_G_or_1536, self.currentError)


        def rule_H(self):
            _locals = {'self': self}
            self.locals['H'] = _locals
            def _G_or_1537():
                self._trace(' <He', (12285, 12289), self.input.position)
                _G_exactly_1538, lastError = self.exactly('H')
                self.considerError(lastError, None)
                return (_G_exactly_1538, self.currentError)
            def _G_or_1539():
                self._trace('igit', (12291, 12295), self.input.position)
                _G_exactly_1540, lastError = self.exactly('h')
                self.considerError(lastError, None)
                return (_G_exactly_1540, self.currentError)
            _G_or_1541, lastError = self._or([_G_or_1537, _G_or_1539])
            self.considerError(lastError, 'H')
            return (_G_or_1541, self.currentError)


        def rule_I(self):
            _locals = {'self': self}
            self.locals['I'] = _locals
            def _G_or_1542():
                self._trace(' -> ', (12300, 12304), self.input.position)
                _G_exactly_1543, lastError = self.exactly('I')
                self.considerError(lastError, None)
                return (_G_exactly_1543, self.currentError)
            def _G_or_1544():
                self._trace('t(ds', (12306, 12310), self.input.position)
                _G_exactly_1545, lastError = self.exactly('i')
                self.considerError(lastError, None)
                return (_G_exactly_1545, self.currentError)
            _G_or_1546, lastError = self._or([_G_or_1542, _G_or_1544])
            self.considerError(lastError, 'I')
            return (_G_or_1546, self.currentError)


        def rule_K(self):
            _locals = {'self': self}
            self.locals['K'] = _locals
            def _G_or_1547():
                self._trace('\n\n  ', (12315, 12319), self.input.position)
                _G_exactly_1548, lastError = self.exactly('K')
                self.considerError(lastError, None)
                return (_G_exactly_1548, self.currentError)
            def _G_or_1549():
                self._trace('Deci', (12321, 12325), self.input.position)
                _G_exactly_1550, lastError = self.exactly('k')
                self.considerError(lastError, None)
                return (_G_exactly_1550, self.currentError)
            _G_or_1551, lastError = self._or([_G_or_1547, _G_or_1549])
            self.considerError(lastError, 'K')
            return (_G_or_1551, self.currentError)


        def rule_L(self):
            _locals = {'self': self}
            self.locals['L'] = _locals
            def _G_or_1552():
                self._trace('tege', (12330, 12334), self.input.position)
                _G_exactly_1553, lastError = self.exactly('L')
                self.considerError(lastError, None)
                return (_G_exactly_1553, self.currentError)
            def _G_or_1554():
                self._trace('= <d', (12336, 12340), self.input.position)
                _G_exactly_1555, lastError = self.exactly('l')
                self.considerError(lastError, None)
                return (_G_exactly_1555, self.currentError)
            _G_or_1556, lastError = self._or([_G_or_1552, _G_or_1554])
            self.considerError(lastError, 'L')
            return (_G_or_1556, self.currentError)


        def rule_M(self):
            _locals = {'self': self}
            self.locals['M'] = _locals
            def _G_or_1557():
                self._trace('>:ds', (12345, 12349), self.input.position)
                _G_exactly_1558, lastError = self.exactly('M')
                self.considerError(lastError, None)
                return (_G_exactly_1558, self.currentError)
            def _G_or_1559():
                self._trace('> in', (12351, 12355), self.input.position)
                _G_exactly_1560, lastError = self.exactly('m')
                self.considerError(lastError, None)
                return (_G_exactly_1560, self.currentError)
            _G_or_1561, lastError = self._or([_G_or_1557, _G_or_1559])
            self.considerError(lastError, 'M')
            return (_G_or_1561, self.currentError)


        def rule_N(self):
            _locals = {'self': self}
            self.locals['N'] = _locals
            def _G_or_1562():
                self._trace('\n\n  ', (12360, 12364), self.input.position)
                _G_exactly_1563, lastError = self.exactly('N')
                self.considerError(lastError, None)
                return (_G_exactly_1563, self.currentError)
            def _G_or_1564():
                self._trace('Doub', (12366, 12370), self.input.position)
                _G_exactly_1565, lastError = self.exactly('n')
                self.considerError(lastError, None)
                return (_G_exactly_1565, self.currentError)
            _G_or_1566, lastError = self._or([_G_or_1562, _G_or_1564])
            self.considerError(lastError, 'N')
            return (_G_or_1566, self.currentError)


        def rule_O(self):
            _locals = {'self': self}
            self.locals['O'] = _locals
            def _G_or_1567():
                self._trace('eral', (12375, 12379), self.input.position)
                _G_exactly_1568, lastError = self.exactly('O')
                self.considerError(lastError, None)
                return (_G_exactly_1568, self.currentError)
            def _G_or_1569():
                self._trace(' Exp', (12381, 12385), self.input.position)
                _G_exactly_1570, lastError = self.exactly('o')
                self.considerError(lastError, None)
                return (_G_exactly_1570, self.currentError)
            _G_or_1571, lastError = self._or([_G_or_1567, _G_or_1569])
            self.considerError(lastError, 'O')
            return (_G_or_1571, self.currentError)


        def rule_P(self):
            _locals = {'self': self}
            self.locals['P'] = _locals
            def _G_or_1572():
                self._trace('Deci', (12390, 12394), self.input.position)
                _G_exactly_1573, lastError = self.exactly('P')
                self.considerError(lastError, None)
                return (_G_exactly_1573, self.currentError)
            def _G_or_1574():
                self._trace('lRea', (12396, 12400), self.input.position)
                _G_exactly_1575, lastError = self.exactly('p')
                self.considerError(lastError, None)
                return (_G_exactly_1575, self.currentError)
            _G_or_1576, lastError = self._or([_G_or_1572, _G_or_1574])
            self.considerError(lastError, 'P')
            return (_G_or_1576, self.currentError)


        def rule_R(self):
            _locals = {'self': self}
            self.locals['R'] = _locals
            def _G_or_1577():
                self._trace('    ', (12405, 12409), self.input.position)
                _G_exactly_1578, lastError = self.exactly('R')
                self.considerError(lastError, None)
                return (_G_exactly_1578, self.currentError)
            def _G_or_1579():
                self._trace('    ', (12411, 12415), self.input.position)
                _G_exactly_1580, lastError = self.exactly('r')
                self.considerError(lastError, None)
                return (_G_exactly_1580, self.currentError)
            _G_or_1581, lastError = self._or([_G_or_1577, _G_or_1579])
            self.considerError(lastError, 'R')
            return (_G_or_1581, self.currentError)


        def rule_S(self):
            _locals = {'self': self}
            self.locals['S'] = _locals
            def _G_or_1582():
                self._trace('| Re', (12420, 12424), self.input.position)
                _G_exactly_1583, lastError = self.exactly('S')
                self.considerError(lastError, None)
                return (_G_exactly_1583, self.currentError)
            def _G_or_1584():
                self._trace('larD', (12426, 12430), self.input.position)
                _G_exactly_1585, lastError = self.exactly('s')
                self.considerError(lastError, None)
                return (_G_exactly_1585, self.currentError)
            _G_or_1586, lastError = self._or([_G_or_1582, _G_or_1584])
            self.considerError(lastError, 'S')
            return (_G_or_1586, self.currentError)


        def rule_T(self):
            _locals = {'self': self}
            self.locals['T'] = _locals
            def _G_or_1587():
                self._trace('lRea', (12435, 12439), self.input.position)
                _G_exactly_1588, lastError = self.exactly('T')
                self.considerError(lastError, None)
                return (_G_exactly_1588, self.currentError)
            def _G_or_1589():
                self._trace('\n   ', (12441, 12445), self.input.position)
                _G_exactly_1590, lastError = self.exactly('t')
                self.considerError(lastError, None)
                return (_G_exactly_1590, self.currentError)
            _G_or_1591, lastError = self._or([_G_or_1587, _G_or_1589])
            self.considerError(lastError, 'T')
            return (_G_or_1591, self.currentError)


        def rule_U(self):
            _locals = {'self': self}
            self.locals['U'] = _locals
            def _G_or_1592():
                self._trace('nent', (12450, 12454), self.input.position)
                _G_exactly_1593, lastError = self.exactly('U')
                self.considerError(lastError, None)
                return (_G_exactly_1593, self.currentError)
            def _G_or_1594():
                self._trace('cima', (12456, 12460), self.input.position)
                _G_exactly_1595, lastError = self.exactly('u')
                self.considerError(lastError, None)
                return (_G_exactly_1595, self.currentError)
            _G_or_1596, lastError = self._or([_G_or_1592, _G_or_1594])
            self.considerError(lastError, 'U')
            return (_G_or_1596, self.currentError)


        def rule_V(self):
            _locals = {'self': self}
            self.locals['V'] = _locals
            def _G_or_1597():
                self._trace(' = <', (12465, 12469), self.input.position)
                _G_exactly_1598, lastError = self.exactly('V')
                self.considerError(lastError, None)
                return (_G_exactly_1598, self.currentError)
            def _G_or_1599():
                self._trace('egul', (12471, 12475), self.input.position)
                _G_exactly_1600, lastError = self.exactly('v')
                self.considerError(lastError, None)
                return (_G_exactly_1600, self.currentError)
            _G_or_1601, lastError = self._or([_G_or_1597, _G_or_1599])
            self.considerError(lastError, 'V')
            return (_G_or_1601, self.currentError)


        def rule_W(self):
            _locals = {'self': self}
            self.locals['W'] = _locals
            def _G_or_1602():
                self._trace('imal', (12480, 12484), self.input.position)
                _G_exactly_1603, lastError = self.exactly('W')
                self.considerError(lastError, None)
                return (_G_exactly_1603, self.currentError)
            def _G_or_1604():
                self._trace('al |', (12486, 12490), self.input.position)
                _G_exactly_1605, lastError = self.exactly('w')
                self.considerError(lastError, None)
                return (_G_exactly_1605, self.currentError)
            _G_or_1606, lastError = self._or([_G_or_1602, _G_or_1604])
            self.considerError(lastError, 'W')
            return (_G_or_1606, self.currentError)


        def rule_X(self):
            _locals = {'self': self}
            self.locals['X'] = _locals
            def _G_or_1607():
                self._trace('malI', (12495, 12499), self.input.position)
                _G_exactly_1608, lastError = self.exactly('X')
                self.considerError(lastError, None)
                return (_G_exactly_1608, self.currentError)
            def _G_or_1609():
                self._trace('eger', (12501, 12505), self.input.position)
                _G_exactly_1610, lastError = self.exactly('x')
                self.considerError(lastError, None)
                return (_G_exactly_1610, self.currentError)
            _G_or_1611, lastError = self._or([_G_or_1607, _G_or_1609])
            self.considerError(lastError, 'X')
            return (_G_or_1611, self.currentError)


        def rule_Y(self):
            _locals = {'self': self}
            self.locals['Y'] = _locals
            def _G_or_1612():
                self._trace("'+' ", (12510, 12514), self.input.position)
                _G_exactly_1613, lastError = self.exactly('Y')
                self.considerError(lastError, None)
                return (_G_exactly_1613, self.currentError)
            def _G_or_1614():
                self._trace("'-')", (12516, 12520), self.input.position)
                _G_exactly_1615, lastError = self.exactly('y')
                self.considerError(lastError, None)
                return (_G_exactly_1615, self.currentError)
            _G_or_1616, lastError = self._or([_G_or_1612, _G_or_1614])
            self.considerError(lastError, 'Y')
            return (_G_or_1616, self.currentError)


        def rule_Z(self):
            _locals = {'self': self}
            self.locals['Z'] = _locals
            def _G_or_1617():
                self._trace('imal', (12525, 12529), self.input.position)
                _G_exactly_1618, lastError = self.exactly('Z')
                self.considerError(lastError, None)
                return (_G_exactly_1618, self.currentError)
            def _G_or_1619():
                self._trace('tege', (12531, 12535), self.input.position)
                _G_exactly_1620, lastError = self.exactly('z')
                self.considerError(lastError, None)
                return (_G_exactly_1620, self.currentError)
            _G_or_1621, lastError = self._or([_G_or_1617, _G_or_1619])
            self.considerError(lastError, 'Z')
            return (_G_or_1621, self.currentError)


        _G_expr_9 = compile('s', '<string>', 'eval')
        _G_expr_27 = compile('["UnionAll", sq, rq]', '<string>', 'eval')
        _G_expr_39 = compile('["Union", sq, rq]', '<string>', 'eval')
        _G_expr_55 = compile('["SingleQuery", m, w, r]', '<string>', 'eval')
        _G_expr_69 = compile('["StrictMatch", p, w]', '<string>', 'eval')
        _G_expr_92 = compile('["OptionalMatch", p, w]', '<string>', 'eval')
        _G_expr_99 = compile('["Match", head] + tail', '<string>', 'eval')
        _G_expr_114 = compile('["Unwind", ex, v]', '<string>', 'eval')
        _G_expr_127 = compile('["Merge", [head] + tail]', '<string>', 'eval')
        _G_expr_140 = compile('["MergeActionMatch", s]', '<string>', 'eval')
        _G_expr_154 = compile('["MergeActionCreate", s]', '<string>', 'eval')
        _G_expr_165 = compile('["Create", p]', '<string>', 'eval')
        _G_expr_178 = compile('["Set", [head] + tail]', '<string>', 'eval')
        _G_expr_184 = compile('["SetItemPropertyExpression", pex, ex]', '<string>', 'eval')
        _G_expr_190 = compile('["SetItem", v, ex]', '<string>', 'eval')
        _G_expr_225 = compile('["Delete", [head] + tail]', '<string>', 'eval')
        _G_expr_241 = compile('["Remove", [head] + tail]', '<string>', 'eval')
        _G_expr_246 = compile('["RemoveItemVar", v, nl]', '<string>', 'eval')
        _G_expr_250 = compile('["RemoveItemPe", p]', '<string>', 'eval')
        _G_expr_275 = compile('["With", d, rb, w]', '<string>', 'eval')
        _G_expr_297 = compile('["Return", d, rb]', '<string>', 'eval')
        _G_expr_315 = compile('["ReturnBody", ri, o, s, l]', '<string>', 'eval')
        _G_expr_328 = compile('["ReturnItems", [head] + tail]', '<string>', 'eval')
        _G_expr_337 = compile('["ReturnItem", ex, s]', '<string>', 'eval')
        _G_expr_341 = compile('["ReturnItem", ex, None]', '<string>', 'eval')
        _G_expr_360 = compile('["Order", [head] + tail]', '<string>', 'eval')
        _G_expr_368 = compile('["Skip", ex]', '<string>', 'eval')
        _G_expr_377 = compile('["Limit", ex]', '<string>', 'eval')
        _G_expr_400 = compile('["sort", ex, "desc"]', '<string>', 'eval')
        _G_expr_424 = compile('["sort", ex, "asc"]', '<string>', 'eval')
        _G_expr_434 = compile('["Where", ex]', '<string>', 'eval')
        _G_expr_442 = compile('[head] + tail', '<string>', 'eval')
        _G_expr_450 = compile('["PatternPart", v, ap]', '<string>', 'eval')
        _G_expr_457 = compile('["GraphPatternPart", v, ap]', '<string>', 'eval')
        _G_expr_461 = compile('["PatternPart", None, ap]', '<string>', 'eval')
        _G_expr_471 = compile('["PatternElement", np, pec]', '<string>', 'eval')
        _G_expr_477 = compile('pe', '<string>', 'eval')
        _G_expr_491 = compile('nl', '<string>', 'eval')
        _G_expr_498 = compile('p', '<string>', 'eval')
        _G_expr_503 = compile('["NodePattern", s, nl, p]', '<string>', 'eval')
        _G_expr_508 = compile('["PatternElementChain", rp, np]', '<string>', 'eval')
        _G_expr_528 = compile('["RelationshipsPattern", la, rd, ra]', '<string>', 'eval')
        _G_expr_554 = compile('["RelationshipDetail", v, q, rt, rl, p]', '<string>', 'eval')
        _G_expr_573 = compile('["RelationshipTypes", head] + tail', '<string>', 'eval')
        _G_expr_583 = compile('["NodeLabel", n]', '<string>', 'eval')
        _G_expr_598 = compile('slice(start, stop)', '<string>', 'eval')
        _G_expr_610 = compile('["or", ex1, ex2]', '<string>', 'eval')
        _G_expr_623 = compile('["xor", ex1, ex2]', '<string>', 'eval')
        _G_expr_636 = compile('["and", ex1, ex2]', '<string>', 'eval')
        _G_expr_647 = compile('["not", ex]', '<string>', 'eval')
        _G_expr_658 = compile('["eq",  ex1, ex2]', '<string>', 'eval')
        _G_expr_666 = compile('["neq", ex1, ex2]', '<string>', 'eval')
        _G_expr_681 = compile('["lt",  ex1, ex2]', '<string>', 'eval')
        _G_expr_689 = compile('["gt",  ex1, ex2]', '<string>', 'eval')
        _G_expr_697 = compile('["lte", ex1, ex2]', '<string>', 'eval')
        _G_expr_705 = compile('["gte", ex1, ex2]', '<string>', 'eval')
        _G_expr_716 = compile('["add", ex1, ex2]', '<string>', 'eval')
        _G_expr_724 = compile('["sub", ex1, ex2]', '<string>', 'eval')
        _G_expr_735 = compile('["multi", ex1, ex2]', '<string>', 'eval')
        _G_expr_743 = compile('["div",   ex1, ex2]', '<string>', 'eval')
        _G_expr_751 = compile('["mod",   ex1, ex2]', '<string>', 'eval')
        _G_expr_762 = compile('["hat", ex1, ex2]', '<string>', 'eval')
        _G_expr_775 = compile('["minus", ex]', '<string>', 'eval')
        _G_expr_788 = compile('["PropertyLookup", prop_name]', '<string>', 'eval')
        _G_expr_803 = compile('["slice", start, end]', '<string>', 'eval')
        _G_expr_855 = compile('[operator, ex2]', '<string>', 'eval')
        _G_expr_883 = compile('["Expression3", ex1, c]', '<string>', 'eval')
        _G_expr_897 = compile('["Expression2", a, c]', '<string>', 'eval')
        _G_expr_954 = compile('item', '<string>', 'eval')
        _G_expr_962 = compile('["List", ex]', '<string>', 'eval')
        _G_expr_977 = compile('["Filter", fex]', '<string>', 'eval')
        _G_expr_999 = compile('["Extract", fex, ex]', '<string>', 'eval')
        _G_expr_1011 = compile('["All", fex]', '<string>', 'eval')
        _G_expr_1023 = compile('["Any", fex]', '<string>', 'eval')
        _G_expr_1036 = compile('["None", fex]', '<string>', 'eval')
        _G_expr_1051 = compile('["Single", fex]', '<string>', 'eval')
        _G_expr_1069 = compile('ex', '<string>', 'eval')
        _G_expr_1077 = compile('["RelationshipsPattern", np, pec]', '<string>', 'eval')
        _G_expr_1088 = compile('["GraphRelationshipsPattern", v, np, pec]', '<string>', 'eval')
        _G_expr_1096 = compile('["FilterExpression", i, w]', '<string>', 'eval')
        _G_expr_1104 = compile('["IdInColl", v, ex]', '<string>', 'eval')
        _G_expr_1136 = compile('["call", func, distinct, args]', '<string>', 'eval')
        _G_expr_1148 = compile('["ListComprehension", fex, ex]', '<string>', 'eval')
        _G_expr_1154 = compile('["PropertyLookup", n]', '<string>', 'eval')
        _G_expr_1183 = compile('["Case", ex, cas, el]', '<string>', 'eval')
        _G_expr_1198 = compile('[ex1, ex2]', '<string>', 'eval')
        _G_expr_1201 = compile('["Variable", s]', '<string>', 'eval')
        _G_expr_1220 = compile('"".join(cs)', '<string>', 'eval')
        _G_expr_1241 = compile('["Literal", l]', '<string>', 'eval')
        _G_expr_1283 = compile('(k, v)', '<string>', 'eval')
        _G_expr_1302 = compile('["Literal", dict(pairs)]', '<string>', 'eval')
        _G_expr_1310 = compile('["Parameter", p]', '<string>', 'eval')
        _G_expr_1317 = compile('["Expression", a, opts]', '<string>', 'eval')
        _G_expr_1341 = compile('int(ds, 8)', '<string>', 'eval')
        _G_expr_1365 = compile('int(ds, 16)', '<string>', 'eval')
        _G_expr_1372 = compile('int(ds)', '<string>', 'eval')
        _G_expr_1396 = compile('float(ds)', '<string>', 'eval')
    if Grammar.globals is not None:
        Grammar.globals = Grammar.globals.copy()
        Grammar.globals.update(ruleGlobals)
    else:
        Grammar.globals = ruleGlobals
    return Grammar