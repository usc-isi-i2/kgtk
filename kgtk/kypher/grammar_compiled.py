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
                self._trace('ov', (2070, 2072), self.input.position)
                _G_apply_272, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('eItemV', (2072, 2078), self.input.position)
                _G_apply_273, lastError = self._apply(self.rule_Where, "Where", [])
                self.considerError(lastError, None)
                return (_G_apply_273, self.currentError)
            def _G_optional_274():
                return (None, self.input.nullError())
            _G_or_275, lastError = self._or([_G_optional_271, _G_optional_274])
            self.considerError(lastError, 'With')
            _locals['w'] = _G_or_275
            _G_python_277, lastError = eval(self._G_expr_276, self.globals, _locals), None
            self.considerError(lastError, 'With')
            return (_G_python_277, self.currentError)


        def rule_Return(self):
            _locals = {'self': self}
            self.locals['Return'] = _locals
            self._trace('ty', (2114, 2116), self.input.position)
            _G_apply_278, lastError = self._apply(self.rule_R, "R", [])
            self.considerError(lastError, 'Return')
            self._trace('Ex', (2116, 2118), self.input.position)
            _G_apply_279, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'Return')
            self._trace('pr', (2118, 2120), self.input.position)
            _G_apply_280, lastError = self._apply(self.rule_T, "T", [])
            self.considerError(lastError, 'Return')
            self._trace('es', (2120, 2122), self.input.position)
            _G_apply_281, lastError = self._apply(self.rule_U, "U", [])
            self.considerError(lastError, 'Return')
            self._trace('si', (2122, 2124), self.input.position)
            _G_apply_282, lastError = self._apply(self.rule_R, "R", [])
            self.considerError(lastError, 'Return')
            self._trace('on', (2124, 2126), self.input.position)
            _G_apply_283, lastError = self._apply(self.rule_N, "N", [])
            self.considerError(lastError, 'Return')
            def _G_optional_284():
                self._trace(' -', (2128, 2130), self.input.position)
                _G_apply_285, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('> ', (2130, 2132), self.input.position)
                _G_apply_286, lastError = self._apply(self.rule_D, "D", [])
                self.considerError(lastError, None)
                self._trace('["', (2132, 2134), self.input.position)
                _G_apply_287, lastError = self._apply(self.rule_I, "I", [])
                self.considerError(lastError, None)
                self._trace('Re', (2134, 2136), self.input.position)
                _G_apply_288, lastError = self._apply(self.rule_S, "S", [])
                self.considerError(lastError, None)
                self._trace('mo', (2136, 2138), self.input.position)
                _G_apply_289, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                self._trace('ve', (2138, 2140), self.input.position)
                _G_apply_290, lastError = self._apply(self.rule_I, "I", [])
                self.considerError(lastError, None)
                self._trace('It', (2140, 2142), self.input.position)
                _G_apply_291, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace('em', (2142, 2144), self.input.position)
                _G_apply_292, lastError = self._apply(self.rule_C, "C", [])
                self.considerError(lastError, None)
                self._trace('Pe', (2144, 2146), self.input.position)
                _G_apply_293, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                return (_G_apply_293, self.currentError)
            def _G_optional_294():
                return (None, self.input.nullError())
            _G_or_295, lastError = self._or([_G_optional_284, _G_optional_294])
            self.considerError(lastError, 'Return')
            _locals['d'] = _G_or_295
            self._trace(']\n\n', (2150, 2153), self.input.position)
            _G_apply_296, lastError = self._apply(self.rule_SP, "SP", [])
            self.considerError(lastError, 'Return')
            self._trace('    With = ', (2153, 2164), self.input.position)
            _G_apply_297, lastError = self._apply(self.rule_ReturnBody, "ReturnBody", [])
            self.considerError(lastError, 'Return')
            _locals['rb'] = _G_apply_297
            _G_python_299, lastError = eval(self._G_expr_298, self.globals, _locals), None
            self.considerError(lastError, 'Return')
            return (_G_python_299, self.currentError)


        def rule_ReturnBody(self):
            _locals = {'self': self}
            self.locals['ReturnBody'] = _locals
            self._trace('urnBody:rb (', (2202, 2214), self.input.position)
            _G_apply_300, lastError = self._apply(self.rule_ReturnItems, "ReturnItems", [])
            self.considerError(lastError, 'ReturnBody')
            _locals['ri'] = _G_apply_300
            def _G_optional_301():
                self._trace('er', (2219, 2221), self.input.position)
                _G_apply_302, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('e)?:w ', (2221, 2227), self.input.position)
                _G_apply_303, lastError = self._apply(self.rule_Order, "Order", [])
                self.considerError(lastError, None)
                return (_G_apply_303, self.currentError)
            def _G_optional_304():
                return (None, self.input.nullError())
            _G_or_305, lastError = self._or([_G_optional_301, _G_optional_304])
            self.considerError(lastError, 'ReturnBody')
            _locals['o'] = _G_or_305
            def _G_optional_306():
                self._trace('it', (2233, 2235), self.input.position)
                _G_apply_307, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('h", d', (2235, 2240), self.input.position)
                _G_apply_308, lastError = self._apply(self.rule_Skip, "Skip", [])
                self.considerError(lastError, None)
                return (_G_apply_308, self.currentError)
            def _G_optional_309():
                return (None, self.input.nullError())
            _G_or_310, lastError = self._or([_G_optional_306, _G_optional_309])
            self.considerError(lastError, 'ReturnBody')
            _locals['s'] = _G_or_310
            def _G_optional_311():
                self._trace('w]', (2246, 2248), self.input.position)
                _G_apply_312, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('\n\n    ', (2248, 2254), self.input.position)
                _G_apply_313, lastError = self._apply(self.rule_Limit, "Limit", [])
                self.considerError(lastError, None)
                return (_G_apply_313, self.currentError)
            def _G_optional_314():
                return (None, self.input.nullError())
            _G_or_315, lastError = self._or([_G_optional_311, _G_optional_314])
            self.considerError(lastError, 'ReturnBody')
            _locals['l'] = _G_or_315
            _G_python_317, lastError = eval(self._G_expr_316, self.globals, _locals), None
            self.considerError(lastError, 'ReturnBody')
            return (_G_python_317, self.currentError)


        def rule_ReturnItems(self):
            _locals = {'self': self}
            self.locals['ReturnItems'] = _locals
            def _G_or_318():
                self._trace('rnB', (2306, 2309), self.input.position)
                _G_exactly_319, lastError = self.exactly('*')
                self.considerError(lastError, None)
                return (_G_exactly_319, self.currentError)
            def _G_or_320():
                self._trace('y:rb -> ["R', (2311, 2322), self.input.position)
                _G_apply_321, lastError = self._apply(self.rule_ReturnItem, "ReturnItem", [])
                self.considerError(lastError, None)
                return (_G_apply_321, self.currentError)
            _G_or_322, lastError = self._or([_G_or_318, _G_or_320])
            self.considerError(lastError, 'ReturnItems')
            _locals['head'] = _G_or_322
            def _G_many_323():
                self._trace('Re', (2342, 2344), self.input.position)
                _G_apply_324, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('turn', (2344, 2348), self.input.position)
                _G_exactly_325, lastError = self.exactly(',')
                self.considerError(lastError, None)
                self._trace('Bod', (2348, 2351), self.input.position)
                _G_apply_326, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('y = ReturnI', (2351, 2362), self.input.position)
                _G_apply_327, lastError = self._apply(self.rule_ReturnItem, "ReturnItem", [])
                self.considerError(lastError, None)
                return (_G_apply_327, self.currentError)
            _G_many_328, lastError = self.many(_G_many_323)
            self.considerError(lastError, 'ReturnItems')
            _locals['tail'] = _G_many_328
            _G_python_330, lastError = eval(self._G_expr_329, self.globals, _locals), None
            self.considerError(lastError, 'ReturnItems')
            return (_G_python_330, self.currentError)


        def rule_ReturnItem(self):
            _locals = {'self': self}
            self.locals['ReturnItem'] = _locals
            def _G_or_331():
                self._trace('turnBody", ', (2418, 2429), self.input.position)
                _G_apply_332, lastError = self._apply(self.rule_Expression, "Expression", [])
                self.considerError(lastError, None)
                _locals['ex'] = _G_apply_332
                self._trace(' o,', (2432, 2435), self.input.position)
                _G_apply_333, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace(' s', (2435, 2437), self.input.position)
                _G_apply_334, lastError = self._apply(self.rule_A, "A", [])
                self.considerError(lastError, None)
                self._trace(', ', (2437, 2439), self.input.position)
                _G_apply_335, lastError = self._apply(self.rule_S, "S", [])
                self.considerError(lastError, None)
                self._trace('l]\n', (2439, 2442), self.input.position)
                _G_apply_336, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('\n    ReturnIt', (2442, 2455), self.input.position)
                _G_apply_337, lastError = self._apply(self.rule_SymbolicName, "SymbolicName", [])
                self.considerError(lastError, None)
                _locals['s'] = _G_apply_337
                _G_python_339, lastError = eval(self._G_expr_338, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_339, self.currentError)
            def _G_or_340():
                self._trace("      (WS '", (2495, 2506), self.input.position)
                _G_apply_341, lastError = self._apply(self.rule_Expression, "Expression", [])
                self.considerError(lastError, None)
                _locals['ex'] = _G_apply_341
                _G_python_343, lastError = eval(self._G_expr_342, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_343, self.currentError)
            _G_or_344, lastError = self._or([_G_or_331, _G_or_340])
            self.considerError(lastError, 'ReturnItem')
            return (_G_or_344, self.currentError)


        def rule_Order(self):
            _locals = {'self': self}
            self.locals['Order'] = _locals
            self._trace('s",', (2546, 2549), self.input.position)
            _G_apply_345, lastError = self._apply(self.rule_O, "O", [])
            self.considerError(lastError, 'Order')
            self._trace(' [', (2549, 2551), self.input.position)
            _G_apply_346, lastError = self._apply(self.rule_R, "R", [])
            self.considerError(lastError, 'Order')
            self._trace('he', (2551, 2553), self.input.position)
            _G_apply_347, lastError = self._apply(self.rule_D, "D", [])
            self.considerError(lastError, 'Order')
            self._trace('ad', (2553, 2555), self.input.position)
            _G_apply_348, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'Order')
            self._trace('] ', (2555, 2557), self.input.position)
            _G_apply_349, lastError = self._apply(self.rule_R, "R", [])
            self.considerError(lastError, 'Order')
            self._trace('+ t', (2557, 2560), self.input.position)
            _G_apply_350, lastError = self._apply(self.rule_SP, "SP", [])
            self.considerError(lastError, 'Order')
            self._trace('ai', (2560, 2562), self.input.position)
            _G_apply_351, lastError = self._apply(self.rule_B, "B", [])
            self.considerError(lastError, 'Order')
            self._trace('l]', (2562, 2564), self.input.position)
            _G_apply_352, lastError = self._apply(self.rule_Y, "Y", [])
            self.considerError(lastError, 'Order')
            self._trace('\n\n ', (2564, 2567), self.input.position)
            _G_apply_353, lastError = self._apply(self.rule_SP, "SP", [])
            self.considerError(lastError, 'Order')
            self._trace('   Return', (2567, 2576), self.input.position)
            _G_apply_354, lastError = self._apply(self.rule_SortItem, "SortItem", [])
            self.considerError(lastError, 'Order')
            _locals['head'] = _G_apply_354
            def _G_many_355():
                self._trace('Ex', (2583, 2585), self.input.position)
                _G_apply_356, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('pres', (2585, 2589), self.input.position)
                _G_exactly_357, lastError = self.exactly(',')
                self.considerError(lastError, None)
                self._trace('sio', (2589, 2592), self.input.position)
                _G_apply_358, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('n:ex SP A', (2592, 2601), self.input.position)
                _G_apply_359, lastError = self._apply(self.rule_SortItem, "SortItem", [])
                self.considerError(lastError, None)
                return (_G_apply_359, self.currentError)
            _G_many_360, lastError = self.many(_G_many_355)
            self.considerError(lastError, 'Order')
            _locals['tail'] = _G_many_360
            _G_python_362, lastError = eval(self._G_expr_361, self.globals, _locals), None
            self.considerError(lastError, 'Order')
            return (_G_python_362, self.currentError)


        def rule_Skip(self):
            _locals = {'self': self}
            self.locals['Skip'] = _locals
            self._trace('s]\n', (2644, 2647), self.input.position)
            _G_apply_363, lastError = self._apply(self.rule_S, "S", [])
            self.considerError(lastError, 'Skip')
            self._trace('  ', (2647, 2649), self.input.position)
            _G_apply_364, lastError = self._apply(self.rule_K, "K", [])
            self.considerError(lastError, 'Skip')
            self._trace('  ', (2649, 2651), self.input.position)
            _G_apply_365, lastError = self._apply(self.rule_I, "I", [])
            self.considerError(lastError, 'Skip')
            self._trace('  ', (2651, 2653), self.input.position)
            _G_apply_366, lastError = self._apply(self.rule_P, "P", [])
            self.considerError(lastError, 'Skip')
            self._trace('   ', (2653, 2656), self.input.position)
            _G_apply_367, lastError = self._apply(self.rule_SP, "SP", [])
            self.considerError(lastError, 'Skip')
            self._trace('      | Exp', (2656, 2667), self.input.position)
            _G_apply_368, lastError = self._apply(self.rule_Expression, "Expression", [])
            self.considerError(lastError, 'Skip')
            _locals['ex'] = _G_apply_368
            _G_python_370, lastError = eval(self._G_expr_369, self.globals, _locals), None
            self.considerError(lastError, 'Skip')
            return (_G_python_370, self.currentError)


        def rule_Limit(self):
            _locals = {'self': self}
            self.locals['Limit'] = _locals
            self._trace(' ex', (2695, 2698), self.input.position)
            _G_apply_371, lastError = self._apply(self.rule_L, "L", [])
            self.considerError(lastError, 'Limit')
            self._trace(', ', (2698, 2700), self.input.position)
            _G_apply_372, lastError = self._apply(self.rule_I, "I", [])
            self.considerError(lastError, 'Limit')
            self._trace('No', (2700, 2702), self.input.position)
            _G_apply_373, lastError = self._apply(self.rule_M, "M", [])
            self.considerError(lastError, 'Limit')
            self._trace('ne', (2702, 2704), self.input.position)
            _G_apply_374, lastError = self._apply(self.rule_I, "I", [])
            self.considerError(lastError, 'Limit')
            self._trace(']\n', (2704, 2706), self.input.position)
            _G_apply_375, lastError = self._apply(self.rule_T, "T", [])
            self.considerError(lastError, 'Limit')
            self._trace('\n  ', (2706, 2709), self.input.position)
            _G_apply_376, lastError = self._apply(self.rule_SP, "SP", [])
            self.considerError(lastError, 'Limit')
            self._trace('  Order =  ', (2709, 2720), self.input.position)
            _G_apply_377, lastError = self._apply(self.rule_Expression, "Expression", [])
            self.considerError(lastError, 'Limit')
            _locals['ex'] = _G_apply_377
            _G_python_379, lastError = eval(self._G_expr_378, self.globals, _locals), None
            self.considerError(lastError, 'Limit')
            return (_G_python_379, self.currentError)


        def rule_SortItem(self):
            _locals = {'self': self}
            self.locals['SortItem'] = _locals
            def _G_or_380():
                self._trace("d (WS ',' W", (2752, 2763), self.input.position)
                _G_apply_381, lastError = self._apply(self.rule_Expression, "Expression", [])
                self.considerError(lastError, None)
                _locals['ex'] = _G_apply_381
                def _G_or_382():
                    self._trace('tI', (2768, 2770), self.input.position)
                    _G_apply_383, lastError = self._apply(self.rule_SP, "SP", [])
                    self.considerError(lastError, None)
                    self._trace('te', (2770, 2772), self.input.position)
                    _G_apply_384, lastError = self._apply(self.rule_D, "D", [])
                    self.considerError(lastError, None)
                    self._trace('m)', (2772, 2774), self.input.position)
                    _G_apply_385, lastError = self._apply(self.rule_E, "E", [])
                    self.considerError(lastError, None)
                    self._trace('*:', (2774, 2776), self.input.position)
                    _G_apply_386, lastError = self._apply(self.rule_S, "S", [])
                    self.considerError(lastError, None)
                    self._trace('ta', (2776, 2778), self.input.position)
                    _G_apply_387, lastError = self._apply(self.rule_C, "C", [])
                    self.considerError(lastError, None)
                    self._trace('il', (2778, 2780), self.input.position)
                    _G_apply_388, lastError = self._apply(self.rule_E, "E", [])
                    self.considerError(lastError, None)
                    self._trace(' -', (2780, 2782), self.input.position)
                    _G_apply_389, lastError = self._apply(self.rule_N, "N", [])
                    self.considerError(lastError, None)
                    self._trace('> ', (2782, 2784), self.input.position)
                    _G_apply_390, lastError = self._apply(self.rule_D, "D", [])
                    self.considerError(lastError, None)
                    self._trace('["', (2784, 2786), self.input.position)
                    _G_apply_391, lastError = self._apply(self.rule_I, "I", [])
                    self.considerError(lastError, None)
                    self._trace('Or', (2786, 2788), self.input.position)
                    _G_apply_392, lastError = self._apply(self.rule_N, "N", [])
                    self.considerError(lastError, None)
                    self._trace('de', (2788, 2790), self.input.position)
                    _G_apply_393, lastError = self._apply(self.rule_G, "G", [])
                    self.considerError(lastError, None)
                    return (_G_apply_393, self.currentError)
                def _G_or_394():
                    self._trace(', [', (2792, 2795), self.input.position)
                    _G_apply_395, lastError = self._apply(self.rule_SP, "SP", [])
                    self.considerError(lastError, None)
                    self._trace('he', (2795, 2797), self.input.position)
                    _G_apply_396, lastError = self._apply(self.rule_D, "D", [])
                    self.considerError(lastError, None)
                    self._trace('ad', (2797, 2799), self.input.position)
                    _G_apply_397, lastError = self._apply(self.rule_E, "E", [])
                    self.considerError(lastError, None)
                    self._trace('] ', (2799, 2801), self.input.position)
                    _G_apply_398, lastError = self._apply(self.rule_S, "S", [])
                    self.considerError(lastError, None)
                    self._trace('+ ', (2801, 2803), self.input.position)
                    _G_apply_399, lastError = self._apply(self.rule_C, "C", [])
                    self.considerError(lastError, None)
                    return (_G_apply_399, self.currentError)
                _G_or_400, lastError = self._or([_G_or_382, _G_or_394])
                self.considerError(lastError, None)
                _G_python_402, lastError = eval(self._G_expr_401, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_402, self.currentError)
            def _G_or_403():
                self._trace('sion:ex -> ', (2839, 2850), self.input.position)
                _G_apply_404, lastError = self._apply(self.rule_Expression, "Expression", [])
                self.considerError(lastError, None)
                _locals['ex'] = _G_apply_404
                def _G_optional_405():
                    def _G_or_406():
                        self._trace('p"', (2855, 2857), self.input.position)
                        _G_apply_407, lastError = self._apply(self.rule_SP, "SP", [])
                        self.considerError(lastError, None)
                        self._trace(', ', (2857, 2859), self.input.position)
                        _G_apply_408, lastError = self._apply(self.rule_A, "A", [])
                        self.considerError(lastError, None)
                        self._trace('ex', (2859, 2861), self.input.position)
                        _G_apply_409, lastError = self._apply(self.rule_S, "S", [])
                        self.considerError(lastError, None)
                        self._trace(']\n', (2861, 2863), self.input.position)
                        _G_apply_410, lastError = self._apply(self.rule_C, "C", [])
                        self.considerError(lastError, None)
                        self._trace('\n ', (2863, 2865), self.input.position)
                        _G_apply_411, lastError = self._apply(self.rule_E, "E", [])
                        self.considerError(lastError, None)
                        self._trace('  ', (2865, 2867), self.input.position)
                        _G_apply_412, lastError = self._apply(self.rule_N, "N", [])
                        self.considerError(lastError, None)
                        self._trace(' L', (2867, 2869), self.input.position)
                        _G_apply_413, lastError = self._apply(self.rule_D, "D", [])
                        self.considerError(lastError, None)
                        self._trace('im', (2869, 2871), self.input.position)
                        _G_apply_414, lastError = self._apply(self.rule_I, "I", [])
                        self.considerError(lastError, None)
                        self._trace('it', (2871, 2873), self.input.position)
                        _G_apply_415, lastError = self._apply(self.rule_N, "N", [])
                        self.considerError(lastError, None)
                        self._trace(' =', (2873, 2875), self.input.position)
                        _G_apply_416, lastError = self._apply(self.rule_G, "G", [])
                        self.considerError(lastError, None)
                        return (_G_apply_416, self.currentError)
                    def _G_or_417():
                        self._trace('L I', (2877, 2880), self.input.position)
                        _G_apply_418, lastError = self._apply(self.rule_SP, "SP", [])
                        self.considerError(lastError, None)
                        self._trace(' M', (2880, 2882), self.input.position)
                        _G_apply_419, lastError = self._apply(self.rule_A, "A", [])
                        self.considerError(lastError, None)
                        self._trace(' I', (2882, 2884), self.input.position)
                        _G_apply_420, lastError = self._apply(self.rule_S, "S", [])
                        self.considerError(lastError, None)
                        self._trace(' T', (2884, 2886), self.input.position)
                        _G_apply_421, lastError = self._apply(self.rule_C, "C", [])
                        self.considerError(lastError, None)
                        return (_G_apply_421, self.currentError)
                    _G_or_422, lastError = self._or([_G_or_406, _G_or_417])
                    self.considerError(lastError, None)
                    return (_G_or_422, self.currentError)
                def _G_optional_423():
                    return (None, self.input.nullError())
                _G_or_424, lastError = self._or([_G_optional_405, _G_optional_423])
                self.considerError(lastError, None)
                _G_python_426, lastError = eval(self._G_expr_425, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_426, self.currentError)
            _G_or_427, lastError = self._or([_G_or_380, _G_or_403])
            self.considerError(lastError, 'SortItem')
            return (_G_or_427, self.currentError)


        def rule_Where(self):
            _locals = {'self': self}
            self.locals['Where'] = _locals
            self._trace('\n\n', (2920, 2922), self.input.position)
            _G_apply_428, lastError = self._apply(self.rule_W, "W", [])
            self.considerError(lastError, 'Where')
            self._trace('  ', (2922, 2924), self.input.position)
            _G_apply_429, lastError = self._apply(self.rule_H, "H", [])
            self.considerError(lastError, 'Where')
            self._trace('  ', (2924, 2926), self.input.position)
            _G_apply_430, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'Where')
            self._trace('So', (2926, 2928), self.input.position)
            _G_apply_431, lastError = self._apply(self.rule_R, "R", [])
            self.considerError(lastError, 'Where')
            self._trace('rt', (2928, 2930), self.input.position)
            _G_apply_432, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'Where')
            self._trace('Ite', (2930, 2933), self.input.position)
            _G_apply_433, lastError = self._apply(self.rule_SP, "SP", [])
            self.considerError(lastError, 'Where')
            self._trace('m = Express', (2933, 2944), self.input.position)
            _G_apply_434, lastError = self._apply(self.rule_Expression, "Expression", [])
            self.considerError(lastError, 'Where')
            _locals['ex'] = _G_apply_434
            _G_python_436, lastError = eval(self._G_expr_435, self.globals, _locals), None
            self.considerError(lastError, 'Where')
            return (_G_python_436, self.currentError)


        def rule_Pattern(self):
            _locals = {'self': self}
            self.locals['Pattern'] = _locals
            self._trace('| SP D E S C', (2975, 2987), self.input.position)
            _G_apply_437, lastError = self._apply(self.rule_PatternPart, "PatternPart", [])
            self.considerError(lastError, 'Pattern')
            _locals['head'] = _G_apply_437
            def _G_many_438():
                self._trace('sor', (2994, 2997), self.input.position)
                _G_exactly_439, lastError = self.exactly(',')
                self.considerError(lastError, None)
                self._trace('t",', (2997, 3000), self.input.position)
                _G_apply_440, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace(' ex, "desc"]', (3000, 3012), self.input.position)
                _G_apply_441, lastError = self._apply(self.rule_PatternPart, "PatternPart", [])
                self.considerError(lastError, None)
                return (_G_apply_441, self.currentError)
            _G_many_442, lastError = self.many(_G_many_438)
            self.considerError(lastError, 'Pattern')
            _locals['tail'] = _G_many_442
            _G_python_444, lastError = eval(self._G_expr_443, self.globals, _locals), None
            self.considerError(lastError, 'Pattern')
            return (_G_python_444, self.currentError)


        def rule_PatternPart(self):
            _locals = {'self': self}
            self.locals['PatternPart'] = _locals
            def _G_or_445():
                self._trace(' N D I N', (3053, 3061), self.input.position)
                _G_apply_446, lastError = self._apply(self.rule_Variable, "Variable", [])
                self.considerError(lastError, None)
                _locals['v'] = _G_apply_446
                self._trace(' | ', (3063, 3066), self.input.position)
                _G_apply_447, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('SP A', (3066, 3070), self.input.position)
                _G_exactly_448, lastError = self.exactly('=')
                self.considerError(lastError, None)
                self._trace(' S ', (3070, 3073), self.input.position)
                _G_apply_449, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('C)? -> ["sort", ex, "', (3073, 3094), self.input.position)
                _G_apply_450, lastError = self._apply(self.rule_AnonymousPatternPart, "AnonymousPatternPart", [])
                self.considerError(lastError, None)
                _locals['ap'] = _G_apply_450
                _G_python_452, lastError = eval(self._G_expr_451, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_452, self.currentError)
            def _G_or_453():
                self._trace('-> ["Whe', (3140, 3148), self.input.position)
                _G_apply_454, lastError = self._apply(self.rule_Variable, "Variable", [])
                self.considerError(lastError, None)
                _locals['v'] = _G_apply_454
                self._trace('", e', (3150, 3154), self.input.position)
                _G_exactly_455, lastError = self.exactly(':')
                self.considerError(lastError, None)
                self._trace('x]\n', (3154, 3157), self.input.position)
                _G_apply_456, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('\n    Pattern = Patter', (3157, 3178), self.input.position)
                _G_apply_457, lastError = self._apply(self.rule_AnonymousPatternPart, "AnonymousPatternPart", [])
                self.considerError(lastError, None)
                _locals['ap'] = _G_apply_457
                _G_python_459, lastError = eval(self._G_expr_458, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_459, self.currentError)
            def _G_or_460():
                self._trace(' tail\n\n    PatternPar', (3227, 3248), self.input.position)
                _G_apply_461, lastError = self._apply(self.rule_AnonymousPatternPart, "AnonymousPatternPart", [])
                self.considerError(lastError, None)
                _locals['ap'] = _G_apply_461
                _G_python_463, lastError = eval(self._G_expr_462, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_463, self.currentError)
            _G_or_464, lastError = self._or([_G_or_445, _G_or_453, _G_or_460])
            self.considerError(lastError, 'PatternPart')
            return (_G_or_464, self.currentError)


        def rule_AnonymousPatternPart(self):
            _locals = {'self': self}
            self.locals['AnonymousPatternPart'] = _locals
            self._trace('PatternPart", v', (3304, 3319), self.input.position)
            _G_apply_465, lastError = self._apply(self.rule_PatternElement, "PatternElement", [])
            self.considerError(lastError, 'AnonymousPatternPart')
            return (_G_apply_465, self.currentError)


        def rule_PatternElement(self):
            _locals = {'self': self}
            self.locals['PatternElement'] = _locals
            def _G_or_466():
                self._trace("  | (Variable:v ':' WS Anonymous", (3339, 3371), self.input.position)
                _G_apply_467, lastError = self._apply(self.rule_NodePattern, "NodePattern", [])
                self.considerError(lastError, None)
                _locals['np'] = _G_apply_467
                def _G_many_468():
                    self._trace('hP', (3396, 3398), self.input.position)
                    _G_apply_469, lastError = self._apply(self.rule_WS, "WS", [])
                    self.considerError(lastError, None)
                    self._trace('atternPart", v, ap]\n', (3398, 3418), self.input.position)
                    _G_apply_470, lastError = self._apply(self.rule_PatternElementChain, "PatternElementChain", [])
                    self.considerError(lastError, None)
                    return (_G_apply_470, self.currentError)
                _G_many_471, lastError = self.many(_G_many_468)
                self.considerError(lastError, None)
                _locals['pec'] = _G_many_471
                _G_python_473, lastError = eval(self._G_expr_472, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_473, self.currentError)
            def _G_or_474():
                self._trace('   A', (3491, 3495), self.input.position)
                _G_exactly_475, lastError = self.exactly('(')
                self.considerError(lastError, None)
                self._trace('nonymousPattern', (3495, 3510), self.input.position)
                _G_apply_476, lastError = self._apply(self.rule_PatternElement, "PatternElement", [])
                self.considerError(lastError, None)
                _locals['pe'] = _G_apply_476
                self._trace('t = ', (3513, 3517), self.input.position)
                _G_exactly_477, lastError = self.exactly(')')
                self.considerError(lastError, None)
                _G_python_479, lastError = eval(self._G_expr_478, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_479, self.currentError)
            _G_or_480, lastError = self._or([_G_or_466, _G_or_474])
            self.considerError(lastError, 'PatternElement')
            return (_G_or_480, self.currentError)


        def rule_NodePattern(self):
            _locals = {'self': self}
            self.locals['NodePattern'] = _locals
            self._trace('atte', (3538, 3542), self.input.position)
            _G_exactly_481, lastError = self.exactly('(')
            self.considerError(lastError, 'NodePattern')
            self._trace('rnE', (3542, 3545), self.input.position)
            _G_apply_482, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'NodePattern')
            def _G_optional_483():
                self._trace('                    NodePatte', (3560, 3589), self.input.position)
                _G_apply_484, lastError = self._apply(self.rule_SymbolicName, "SymbolicName", [])
                self.considerError(lastError, None)
                _locals['s'] = _G_apply_484
                self._trace(':np', (3591, 3594), self.input.position)
                _G_apply_485, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                _G_python_486, lastError = eval(self._G_expr_9, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_486, self.currentError)
            def _G_optional_487():
                return (None, self.input.nullError())
            _G_or_488, lastError = self._or([_G_optional_483, _G_optional_487])
            self.considerError(lastError, 'NodePattern')
            _locals['s'] = _G_or_488
            def _G_optional_489():
                self._trace('ementChain)*:pec\n           ', (3632, 3660), self.input.position)
                _G_apply_490, lastError = self._apply(self.rule_NodeLabels, "NodeLabels", [])
                self.considerError(lastError, None)
                _locals['nl'] = _G_apply_490
                self._trace('   ', (3663, 3666), self.input.position)
                _G_apply_491, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                _G_python_493, lastError = eval(self._G_expr_492, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_493, self.currentError)
            def _G_optional_494():
                return (None, self.input.nullError())
            _G_or_495, lastError = self._or([_G_optional_489, _G_optional_494])
            self.considerError(lastError, 'NodePattern')
            _locals['nl'] = _G_or_495
            def _G_optional_496():
                self._trace("                | '(' Patter", (3706, 3734), self.input.position)
                _G_apply_497, lastError = self._apply(self.rule_Properties, "Properties", [])
                self.considerError(lastError, None)
                _locals['p'] = _G_apply_497
                self._trace('lem', (3736, 3739), self.input.position)
                _G_apply_498, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                _G_python_500, lastError = eval(self._G_expr_499, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_500, self.currentError)
            def _G_optional_501():
                return (None, self.input.nullError())
            _G_or_502, lastError = self._or([_G_optional_496, _G_optional_501])
            self.considerError(lastError, 'NodePattern')
            _locals['p'] = _G_or_502
            self._trace("odePattern = '('", (3762, 3778), self.input.position)
            _G_exactly_503, lastError = self.exactly(')')
            self.considerError(lastError, 'NodePattern')
            _G_python_505, lastError = eval(self._G_expr_504, self.globals, _locals), None
            self.considerError(lastError, 'NodePattern')
            return (_G_python_505, self.currentError)


        def rule_PatternElementChain(self):
            _locals = {'self': self}
            self.locals['PatternElementChain'] = _locals
            self._trace('ame:s WS -> s\n      ', (3830, 3850), self.input.position)
            _G_apply_506, lastError = self._apply(self.rule_RelationshipPattern, "RelationshipPattern", [])
            self.considerError(lastError, 'PatternElementChain')
            _locals['rp'] = _G_apply_506
            self._trace('   ', (3853, 3856), self.input.position)
            _G_apply_507, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'PatternElementChain')
            self._trace('     )?:s\n  ', (3856, 3868), self.input.position)
            _G_apply_508, lastError = self._apply(self.rule_NodePattern, "NodePattern", [])
            self.considerError(lastError, 'PatternElementChain')
            _locals['np'] = _G_apply_508
            _G_python_510, lastError = eval(self._G_expr_509, self.globals, _locals), None
            self.considerError(lastError, 'PatternElementChain')
            return (_G_python_510, self.currentError)


        def rule_RelationshipPattern(self):
            _locals = {'self': self}
            self.locals['RelationshipPattern'] = _locals
            def _G_optional_511():
                self._trace('              ', (3929, 3943), self.input.position)
                _G_apply_512, lastError = self._apply(self.rule_LeftArrowHead, "LeftArrowHead", [])
                self.considerError(lastError, None)
                return (_G_apply_512, self.currentError)
            def _G_optional_513():
                return (None, self.input.nullError())
            _G_or_514, lastError = self._or([_G_optional_511, _G_optional_513])
            self.considerError(lastError, 'RelationshipPattern')
            _locals['la'] = _G_or_514
            self._trace('?:n', (3947, 3950), self.input.position)
            _G_apply_515, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'RelationshipPattern')
            self._trace('l\n   ', (3950, 3955), self.input.position)
            _G_apply_516, lastError = self._apply(self.rule_Dash, "Dash", [])
            self.considerError(lastError, 'RelationshipPattern')
            self._trace('   ', (3955, 3958), self.input.position)
            _G_apply_517, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'RelationshipPattern')
            def _G_optional_518():
                self._trace('           (\n      ', (3958, 3977), self.input.position)
                _G_apply_519, lastError = self._apply(self.rule_RelationshipDetail, "RelationshipDetail", [])
                self.considerError(lastError, None)
                return (_G_apply_519, self.currentError)
            def _G_optional_520():
                return (None, self.input.nullError())
            _G_or_521, lastError = self._or([_G_optional_518, _G_optional_520])
            self.considerError(lastError, 'RelationshipPattern')
            _locals['rd'] = _G_or_521
            self._trace('   ', (3981, 3984), self.input.position)
            _G_apply_522, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'RelationshipPattern')
            self._trace('     ', (3984, 3989), self.input.position)
            _G_apply_523, lastError = self._apply(self.rule_Dash, "Dash", [])
            self.considerError(lastError, 'RelationshipPattern')
            self._trace('   ', (3989, 3992), self.input.position)
            _G_apply_524, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'RelationshipPattern')
            def _G_optional_525():
                self._trace('Properties:p WS', (3992, 4007), self.input.position)
                _G_apply_526, lastError = self._apply(self.rule_RightArrowHead, "RightArrowHead", [])
                self.considerError(lastError, None)
                return (_G_apply_526, self.currentError)
            def _G_optional_527():
                return (None, self.input.nullError())
            _G_or_528, lastError = self._or([_G_optional_525, _G_optional_527])
            self.considerError(lastError, 'RelationshipPattern')
            _locals['ra'] = _G_or_528
            _G_python_530, lastError = eval(self._G_expr_529, self.globals, _locals), None
            self.considerError(lastError, 'RelationshipPattern')
            return (_G_python_530, self.currentError)


        def rule_RelationshipDetail(self):
            _locals = {'self': self}
            self.locals['RelationshipDetail'] = _locals
            self._trace('tern', (4160, 4164), self.input.position)
            _G_exactly_531, lastError = self.exactly('[')
            self.considerError(lastError, 'RelationshipDetail')
            def _G_optional_532():
                self._trace('ElementChain", rp, np]\n\n   ', (4164, 4191), self.input.position)
                _G_apply_533, lastError = self._apply(self.rule_Variable, "Variable", [])
                self.considerError(lastError, None)
                return (_G_apply_533, self.currentError)
            def _G_optional_534():
                return (None, self.input.nullError())
            _G_or_535, lastError = self._or([_G_optional_532, _G_optional_534])
            self.considerError(lastError, 'RelationshipDetail')
            _locals['v'] = _G_or_535
            def _G_optional_536():
                self._trace('lationshipPattern = Le', (4194, 4216), self.input.position)
                _G_exactly_537, lastError = self.exactly('?')
                self.considerError(lastError, None)
                return (_G_exactly_537, self.currentError)
            def _G_optional_538():
                return (None, self.input.nullError())
            _G_or_539, lastError = self._or([_G_optional_536, _G_optional_538])
            self.considerError(lastError, 'RelationshipDetail')
            _locals['q'] = _G_or_539
            def _G_optional_540():
                self._trace('rrowHead?:la WS Dash WS Relationship', (4219, 4255), self.input.position)
                _G_apply_541, lastError = self._apply(self.rule_RelationshipTypes, "RelationshipTypes", [])
                self.considerError(lastError, None)
                return (_G_apply_541, self.currentError)
            def _G_optional_542():
                return (None, self.input.nullError())
            _G_or_543, lastError = self._or([_G_optional_540, _G_optional_542])
            self.considerError(lastError, 'RelationshipDetail')
            _locals['rt'] = _G_or_543
            def _G_optional_544():
                self._trace('ght', (4279, 4282), self.input.position)
                _G_exactly_545, lastError = self.exactly('*')
                self.considerError(lastError, None)
                self._trace('ArrowHead?:ra', (4282, 4295), self.input.position)
                _G_apply_546, lastError = self._apply(self.rule_RangeLiteral, "RangeLiteral", [])
                self.considerError(lastError, None)
                return (_G_apply_546, self.currentError)
            def _G_optional_547():
                return (None, self.input.nullError())
            _G_or_548, lastError = self._or([_G_optional_544, _G_optional_547])
            self.considerError(lastError, 'RelationshipDetail')
            _locals['rl'] = _G_or_548
            self._trace('"Re', (4300, 4303), self.input.position)
            _G_apply_549, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'RelationshipDetail')
            def _G_optional_550():
                self._trace('lationshipsPattern", la, rd, ', (4303, 4332), self.input.position)
                _G_apply_551, lastError = self._apply(self.rule_Properties, "Properties", [])
                self.considerError(lastError, None)
                return (_G_apply_551, self.currentError)
            def _G_optional_552():
                return (None, self.input.nullError())
            _G_or_553, lastError = self._or([_G_optional_550, _G_optional_552])
            self.considerError(lastError, 'RelationshipDetail')
            _locals['p'] = _G_or_553
            self._trace('\n\n    # TO DO: fix WS ', (4335, 4357), self.input.position)
            _G_exactly_554, lastError = self.exactly(']')
            self.considerError(lastError, 'RelationshipDetail')
            _G_python_556, lastError = eval(self._G_expr_555, self.globals, _locals), None
            self.considerError(lastError, 'RelationshipDetail')
            return (_G_python_556, self.currentError)


        def rule_Properties(self):
            _locals = {'self': self}
            self.locals['Properties'] = _locals
            def _G_or_557():
                self._trace(' NodePatter', (4414, 4425), self.input.position)
                _G_apply_558, lastError = self._apply(self.rule_MapLiteral, "MapLiteral", [])
                self.considerError(lastError, None)
                return (_G_apply_558, self.currentError)
            def _G_or_559():
                self._trace('onshipDeta', (4438, 4448), self.input.position)
                _G_apply_560, lastError = self._apply(self.rule_Parameter, "Parameter", [])
                self.considerError(lastError, None)
                return (_G_apply_560, self.currentError)
            _G_or_561, lastError = self._or([_G_or_557, _G_or_559])
            self.considerError(lastError, 'Properties')
            return (_G_or_561, self.currentError)


        def rule_RelationshipTypes(self):
            _locals = {'self': self}
            self.locals['RelationshipTypes'] = _locals
            self._trace('    ', (4469, 4473), self.input.position)
            _G_exactly_562, lastError = self.exactly(':')
            self.considerError(lastError, 'RelationshipTypes')
            self._trace('      Variab', (4473, 4485), self.input.position)
            _G_apply_563, lastError = self._apply(self.rule_RelTypeName, "RelTypeName", [])
            self.considerError(lastError, 'RelationshipTypes')
            _locals['head'] = _G_apply_563
            def _G_many_564():
                self._trace('  ', (4492, 4494), self.input.position)
                _G_apply_565, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('    ', (4494, 4498), self.input.position)
                _G_exactly_566, lastError = self.exactly('|')
                self.considerError(lastError, None)
                def _G_optional_567():
                    self._trace('    ', (4498, 4502), self.input.position)
                    _G_exactly_568, lastError = self.exactly(':')
                    self.considerError(lastError, None)
                    return (_G_exactly_568, self.currentError)
                def _G_optional_569():
                    return (None, self.input.nullError())
                _G_or_570, lastError = self._or([_G_optional_567, _G_optional_569])
                self.considerError(lastError, None)
                self._trace('   ', (4503, 4506), self.input.position)
                _G_apply_571, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace("       '?'?:", (4506, 4518), self.input.position)
                _G_apply_572, lastError = self._apply(self.rule_RelTypeName, "RelTypeName", [])
                self.considerError(lastError, None)
                return (_G_apply_572, self.currentError)
            _G_many_573, lastError = self.many(_G_many_564)
            self.considerError(lastError, 'RelationshipTypes')
            _locals['tail'] = _G_many_573
            _G_python_575, lastError = eval(self._G_expr_574, self.globals, _locals), None
            self.considerError(lastError, 'RelationshipTypes')
            return (_G_python_575, self.currentError)


        def rule_NodeLabels(self):
            _locals = {'self': self}
            self.locals['NodeLabels'] = _locals
            self._trace('         (', (4577, 4587), self.input.position)
            _G_apply_576, lastError = self._apply(self.rule_NodeLabel, "NodeLabel", [])
            self.considerError(lastError, 'NodeLabels')
            _locals['head'] = _G_apply_576
            def _G_many_577():
                self._trace('ge', (4594, 4596), self.input.position)
                _G_apply_578, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('Literal)?:', (4596, 4606), self.input.position)
                _G_apply_579, lastError = self._apply(self.rule_NodeLabel, "NodeLabel", [])
                self.considerError(lastError, None)
                return (_G_apply_579, self.currentError)
            _G_many_580, lastError = self.many(_G_many_577)
            self.considerError(lastError, 'NodeLabels')
            _locals['tail'] = _G_many_580
            _G_python_581, lastError = eval(self._G_expr_443, self.globals, _locals), None
            self.considerError(lastError, 'NodeLabels')
            return (_G_python_581, self.currentError)


        def rule_NodeLabel(self):
            _locals = {'self': self}
            self.locals['NodeLabel'] = _locals
            self._trace('s?:p', (4643, 4647), self.input.position)
            _G_exactly_582, lastError = self.exactly(':')
            self.considerError(lastError, 'NodeLabel')
            self._trace('\n         ', (4647, 4657), self.input.position)
            _G_apply_583, lastError = self._apply(self.rule_LabelName, "LabelName", [])
            self.considerError(lastError, 'NodeLabel')
            _locals['n'] = _G_apply_583
            _G_python_585, lastError = eval(self._G_expr_584, self.globals, _locals), None
            self.considerError(lastError, 'NodeLabel')
            return (_G_python_585, self.currentError)


        def rule_RangeLiteral(self):
            _locals = {'self': self}
            self.locals['RangeLiteral'] = _locals
            def _G_optional_586():
                self._trace('",', (4697, 4699), self.input.position)
                _G_apply_587, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace(' v, q, rt, rl, ', (4699, 4714), self.input.position)
                _G_apply_588, lastError = self._apply(self.rule_IntegerLiteral, "IntegerLiteral", [])
                self.considerError(lastError, None)
                return (_G_apply_588, self.currentError)
            def _G_optional_589():
                return (None, self.input.nullError())
            _G_or_590, lastError = self._or([_G_optional_586, _G_optional_589])
            self.considerError(lastError, 'RangeLiteral')
            _locals['start'] = _G_or_590
            self._trace('Pro', (4722, 4725), self.input.position)
            _G_apply_591, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'RangeLiteral')
            def _G_optional_592():
                self._trace('rtie', (4727, 4731), self.input.position)
                _G_exactly_593, lastError = self.exactly('..')
                self.considerError(lastError, None)
                self._trace('s =', (4731, 4734), self.input.position)
                _G_apply_594, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace(' MapLiteral\n   ', (4734, 4749), self.input.position)
                _G_apply_595, lastError = self._apply(self.rule_IntegerLiteral, "IntegerLiteral", [])
                self.considerError(lastError, None)
                return (_G_apply_595, self.currentError)
            def _G_optional_596():
                return (None, self.input.nullError())
            _G_or_597, lastError = self._or([_G_optional_592, _G_optional_596])
            self.considerError(lastError, 'RangeLiteral')
            _locals['stop'] = _G_or_597
            self._trace('   ', (4756, 4759), self.input.position)
            _G_apply_598, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'RangeLiteral')
            _G_python_600, lastError = eval(self._G_expr_599, self.globals, _locals), None
            self.considerError(lastError, 'RangeLiteral')
            return (_G_python_600, self.currentError)


        def rule_LabelName(self):
            _locals = {'self': self}
            self.locals['LabelName'] = _locals
            self._trace("s = ':' RelTy", (4794, 4807), self.input.position)
            _G_apply_601, lastError = self._apply(self.rule_SymbolicName, "SymbolicName", [])
            self.considerError(lastError, 'LabelName')
            return (_G_apply_601, self.currentError)


        def rule_RelTypeName(self):
            _locals = {'self': self}
            self.locals['RelTypeName'] = _locals
            self._trace(" '|' ':'? WS ", (4822, 4835), self.input.position)
            _G_apply_602, lastError = self._apply(self.rule_SymbolicName, "SymbolicName", [])
            self.considerError(lastError, 'RelTypeName')
            return (_G_apply_602, self.currentError)


        def rule_Expression(self):
            _locals = {'self': self}
            self.locals['Expression'] = _locals
            self._trace('tail -> ["Rel', (4849, 4862), self.input.position)
            _G_apply_603, lastError = self._apply(self.rule_Expression12, "Expression12", [])
            self.considerError(lastError, 'Expression')
            return (_G_apply_603, self.currentError)


        def rule_Expression12(self):
            _locals = {'self': self}
            self.locals['Expression12'] = _locals
            def _G_or_604():
                self._trace(' head] + tail', (4878, 4891), self.input.position)
                _G_apply_605, lastError = self._apply(self.rule_Expression11, "Expression11", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_605
                self._trace('  N', (4895, 4898), self.input.position)
                _G_apply_606, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('od', (4898, 4900), self.input.position)
                _G_apply_607, lastError = self._apply(self.rule_O, "O", [])
                self.considerError(lastError, None)
                self._trace('eL', (4900, 4902), self.input.position)
                _G_apply_608, lastError = self._apply(self.rule_R, "R", [])
                self.considerError(lastError, None)
                self._trace('abe', (4902, 4905), self.input.position)
                _G_apply_609, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('ls = NodeLabe', (4905, 4918), self.input.position)
                _G_apply_610, lastError = self._apply(self.rule_Expression12, "Expression12", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_610
                _G_python_612, lastError = eval(self._G_expr_611, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_612, self.currentError)
            def _G_or_613():
                self._trace(' tail\n\n    No', (4957, 4970), self.input.position)
                _G_apply_614, lastError = self._apply(self.rule_Expression11, "Expression11", [])
                self.considerError(lastError, None)
                return (_G_apply_614, self.currentError)
            _G_or_615, lastError = self._or([_G_or_604, _G_or_613])
            self.considerError(lastError, 'Expression12')
            return (_G_or_615, self.currentError)


        def rule_Expression11(self):
            _locals = {'self': self}
            self.locals['Expression11'] = _locals
            def _G_or_616():
                self._trace('belName:n -> ', (4986, 4999), self.input.position)
                _G_apply_617, lastError = self._apply(self.rule_Expression10, "Expression10", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_617
                self._trace('deL', (5003, 5006), self.input.position)
                _G_apply_618, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('ab', (5006, 5008), self.input.position)
                _G_apply_619, lastError = self._apply(self.rule_X, "X", [])
                self.considerError(lastError, None)
                self._trace('el', (5008, 5010), self.input.position)
                _G_apply_620, lastError = self._apply(self.rule_O, "O", [])
                self.considerError(lastError, None)
                self._trace('",', (5010, 5012), self.input.position)
                _G_apply_621, lastError = self._apply(self.rule_R, "R", [])
                self.considerError(lastError, None)
                self._trace(' n]', (5012, 5015), self.input.position)
                _G_apply_622, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('\n\n    RangeLi', (5015, 5028), self.input.position)
                _G_apply_623, lastError = self._apply(self.rule_Expression11, "Expression11", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_623
                _G_python_625, lastError = eval(self._G_expr_624, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_625, self.currentError)
            def _G_or_626():
                self._trace("..' WS Intege", (5068, 5081), self.input.position)
                _G_apply_627, lastError = self._apply(self.rule_Expression10, "Expression10", [])
                self.considerError(lastError, None)
                return (_G_apply_627, self.currentError)
            _G_or_628, lastError = self._or([_G_or_616, _G_or_626])
            self.considerError(lastError, 'Expression11')
            return (_G_or_628, self.currentError)


        def rule_Expression10(self):
            _locals = {'self': self}
            self.locals['Expression10'] = _locals
            def _G_or_629():
                self._trace('WS -> slice(', (5097, 5109), self.input.position)
                _G_apply_630, lastError = self._apply(self.rule_Expression9, "Expression9", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_630
                self._trace('t, ', (5113, 5116), self.input.position)
                _G_apply_631, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('st', (5116, 5118), self.input.position)
                _G_apply_632, lastError = self._apply(self.rule_A, "A", [])
                self.considerError(lastError, None)
                self._trace('op', (5118, 5120), self.input.position)
                _G_apply_633, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace(')\n', (5120, 5122), self.input.position)
                _G_apply_634, lastError = self._apply(self.rule_D, "D", [])
                self.considerError(lastError, None)
                self._trace('\n  ', (5122, 5125), self.input.position)
                _G_apply_635, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('  LabelName =', (5125, 5138), self.input.position)
                _G_apply_636, lastError = self._apply(self.rule_Expression10, "Expression10", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_636
                _G_python_638, lastError = eval(self._G_expr_637, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_638, self.currentError)
            def _G_or_639():
                self._trace('cName\n\n    E', (5178, 5190), self.input.position)
                _G_apply_640, lastError = self._apply(self.rule_Expression9, "Expression9", [])
                self.considerError(lastError, None)
                return (_G_apply_640, self.currentError)
            _G_or_641, lastError = self._or([_G_or_629, _G_or_639])
            self.considerError(lastError, 'Expression10')
            return (_G_or_641, self.currentError)


        def rule_Expression9(self):
            _locals = {'self': self}
            self.locals['Expression9'] = _locals
            def _G_or_642():
                self._trace('re', (5205, 5207), self.input.position)
                _G_apply_643, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace('ss', (5207, 5209), self.input.position)
                _G_apply_644, lastError = self._apply(self.rule_O, "O", [])
                self.considerError(lastError, None)
                self._trace('io', (5209, 5211), self.input.position)
                _G_apply_645, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                self._trace('n12', (5211, 5214), self.input.position)
                _G_apply_646, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('\n\n    Expres', (5214, 5226), self.input.position)
                _G_apply_647, lastError = self._apply(self.rule_Expression9, "Expression9", [])
                self.considerError(lastError, None)
                _locals['ex'] = _G_apply_647
                _G_python_649, lastError = eval(self._G_expr_648, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_649, self.currentError)
            def _G_or_650():
                self._trace(' SP Expressi', (5258, 5270), self.input.position)
                _G_apply_651, lastError = self._apply(self.rule_Expression8, "Expression8", [])
                self.considerError(lastError, None)
                return (_G_apply_651, self.currentError)
            _G_or_652, lastError = self._or([_G_or_642, _G_or_650])
            self.considerError(lastError, 'Expression9')
            return (_G_or_652, self.currentError)


        def rule_Expression8(self):
            _locals = {'self': self}
            self.locals['Expression8'] = _locals
            def _G_or_653():
                self._trace('r", ex1, ex2', (5285, 5297), self.input.position)
                _G_apply_654, lastError = self._apply(self.rule_Expression7, "Expression7", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_654
                self._trace('   ', (5301, 5304), self.input.position)
                _G_apply_655, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('    ', (5304, 5308), self.input.position)
                _G_exactly_656, lastError = self.exactly('=')
                self.considerError(lastError, None)
                self._trace('    ', (5308, 5312), self.input.position)
                _G_apply_657, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('    | Expres', (5312, 5324), self.input.position)
                _G_apply_658, lastError = self._apply(self.rule_Expression8, "Expression8", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_658
                _G_python_660, lastError = eval(self._G_expr_659, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_660, self.currentError)
            def _G_or_661():
                self._trace(':ex1 SP X O ', (5363, 5375), self.input.position)
                _G_apply_662, lastError = self._apply(self.rule_Expression7, "Expression7", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_662
                self._trace(' Ex', (5379, 5382), self.input.position)
                _G_apply_663, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('press', (5382, 5387), self.input.position)
                _G_exactly_664, lastError = self.exactly('<>')
                self.considerError(lastError, None)
                self._trace('ion', (5387, 5390), self.input.position)
                _G_apply_665, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('11:ex2 -> ["', (5390, 5402), self.input.position)
                _G_apply_666, lastError = self._apply(self.rule_Expression8, "Expression8", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_666
                _G_python_668, lastError = eval(self._G_expr_667, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_668, self.currentError)
            def _G_or_669():
                self._trace('ession10\n\n  ', (5441, 5453), self.input.position)
                _G_apply_670, lastError = self._apply(self.rule_Expression7, "Expression7", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_670
                self._trace('pre', (5457, 5460), self.input.position)
                _G_apply_671, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('ssion', (5460, 5465), self.input.position)
                _G_exactly_672, lastError = self.exactly('!=')
                self.considerError(lastError, None)
                self._trace('10 ', (5465, 5468), self.input.position)
                _G_apply_673, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('= Expression', (5468, 5480), self.input.position)
                _G_apply_674, lastError = self._apply(self.rule_Expression8, "Expression8", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_674
                _G_python_675, lastError = eval(self._G_expr_667, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_675, self.currentError)
            def _G_or_676():
                self._trace('"and", ex1, ', (5519, 5531), self.input.position)
                _G_apply_677, lastError = self._apply(self.rule_Expression7, "Expression7", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_677
                self._trace('\n  ', (5535, 5538), self.input.position)
                _G_apply_678, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('    ', (5538, 5542), self.input.position)
                _G_exactly_679, lastError = self.exactly('<')
                self.considerError(lastError, None)
                self._trace('    ', (5542, 5546), self.input.position)
                _G_apply_680, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('       | Exp', (5546, 5558), self.input.position)
                _G_apply_681, lastError = self._apply(self.rule_Expression8, "Expression8", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_681
                _G_python_683, lastError = eval(self._G_expr_682, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_683, self.currentError)
            def _G_or_684():
                self._trace('pression9:ex', (5597, 5609), self.input.position)
                _G_apply_685, lastError = self._apply(self.rule_Expression7, "Expression7", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_685
                self._trace('["n', (5613, 5616), self.input.position)
                _G_apply_686, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('ot",', (5616, 5620), self.input.position)
                _G_exactly_687, lastError = self.exactly('>')
                self.considerError(lastError, None)
                self._trace(' ex]', (5620, 5624), self.input.position)
                _G_apply_688, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('\n           ', (5624, 5636), self.input.position)
                _G_apply_689, lastError = self._apply(self.rule_Expression8, "Expression8", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_689
                _G_python_691, lastError = eval(self._G_expr_690, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_691, self.currentError)
            def _G_or_692():
                self._trace('xpression7:e', (5675, 5687), self.input.position)
                _G_apply_693, lastError = self._apply(self.rule_Expression7, "Expression7", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_693
                self._trace("S '", (5691, 5694), self.input.position)
                _G_apply_694, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace("='  W", (5694, 5699), self.input.position)
                _G_exactly_695, lastError = self.exactly('<=')
                self.considerError(lastError, None)
                self._trace('S E', (5699, 5702), self.input.position)
                _G_apply_696, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('xpression8:e', (5702, 5714), self.input.position)
                _G_apply_697, lastError = self._apply(self.rule_Expression8, "Expression8", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_697
                _G_python_699, lastError = eval(self._G_expr_698, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_699, self.currentError)
            def _G_or_700():
                self._trace(' | Expressio', (5753, 5765), self.input.position)
                _G_apply_701, lastError = self._apply(self.rule_Expression7, "Expression7", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_701
                self._trace('x1 ', (5769, 5772), self.input.position)
                _G_apply_702, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace("WS '<", (5772, 5777), self.input.position)
                _G_exactly_703, lastError = self.exactly('>=')
                self.considerError(lastError, None)
                self._trace(">' ", (5777, 5780), self.input.position)
                _G_apply_704, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('WS Expressio', (5780, 5792), self.input.position)
                _G_apply_705, lastError = self._apply(self.rule_Expression8, "Expression8", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_705
                _G_python_707, lastError = eval(self._G_expr_706, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_707, self.currentError)
            def _G_or_708():
                self._trace('     | Expre', (5831, 5843), self.input.position)
                _G_apply_709, lastError = self._apply(self.rule_Expression7, "Expression7", [])
                self.considerError(lastError, None)
                return (_G_apply_709, self.currentError)
            _G_or_710, lastError = self._or([_G_or_653, _G_or_661, _G_or_669, _G_or_676, _G_or_684, _G_or_692, _G_or_700, _G_or_708])
            self.considerError(lastError, 'Expression8')
            return (_G_or_710, self.currentError)


        def rule_Expression7(self):
            _locals = {'self': self}
            self.locals['Expression7'] = _locals
            def _G_or_711():
                self._trace("!=' WS Expre", (5858, 5870), self.input.position)
                _G_apply_712, lastError = self._apply(self.rule_Expression6, "Expression6", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_712
                self._trace('n8:', (5874, 5877), self.input.position)
                _G_apply_713, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('ex2 ', (5877, 5881), self.input.position)
                _G_exactly_714, lastError = self.exactly('+')
                self.considerError(lastError, None)
                self._trace('-> ', (5881, 5884), self.input.position)
                _G_apply_715, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('["neq", ex1,', (5884, 5896), self.input.position)
                _G_apply_716, lastError = self._apply(self.rule_Expression7, "Expression7", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_716
                _G_python_718, lastError = eval(self._G_expr_717, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_718, self.currentError)
            def _G_or_719():
                self._trace(" WS '<'  WS ", (5935, 5947), self.input.position)
                _G_apply_720, lastError = self._apply(self.rule_Expression6, "Expression6", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_720
                self._trace('ess', (5951, 5954), self.input.position)
                _G_apply_721, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('ion8', (5954, 5958), self.input.position)
                _G_exactly_722, lastError = self.exactly('-')
                self.considerError(lastError, None)
                self._trace(':ex', (5958, 5961), self.input.position)
                _G_apply_723, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('2 -> ["lt", ', (5961, 5973), self.input.position)
                _G_apply_724, lastError = self._apply(self.rule_Expression7, "Expression7", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_724
                _G_python_726, lastError = eval(self._G_expr_725, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_726, self.currentError)
            def _G_or_727():
                self._trace("7:ex1 WS '>'", (6012, 6024), self.input.position)
                _G_apply_728, lastError = self._apply(self.rule_Expression6, "Expression6", [])
                self.considerError(lastError, None)
                return (_G_apply_728, self.currentError)
            _G_or_729, lastError = self._or([_G_or_711, _G_or_719, _G_or_727])
            self.considerError(lastError, 'Expression7')
            return (_G_or_729, self.currentError)


        def rule_Expression6(self):
            _locals = {'self': self}
            self.locals['Expression6'] = _locals
            def _G_or_730():
                self._trace('8:ex2 -> ["g', (6039, 6051), self.input.position)
                _G_apply_731, lastError = self._apply(self.rule_Expression5, "Expression5", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_731
                self._trace(' ex', (6055, 6058), self.input.position)
                _G_apply_732, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('1, e', (6058, 6062), self.input.position)
                _G_exactly_733, lastError = self.exactly('*')
                self.considerError(lastError, None)
                self._trace('x2]', (6062, 6065), self.input.position)
                _G_apply_734, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('\n           ', (6065, 6077), self.input.position)
                _G_apply_735, lastError = self._apply(self.rule_Expression6, "Expression6", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_735
                _G_python_737, lastError = eval(self._G_expr_736, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_737, self.currentError)
            def _G_or_738():
                self._trace('ion8:ex2 -> ', (6118, 6130), self.input.position)
                _G_apply_739, lastError = self._apply(self.rule_Expression5, "Expression5", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_739
                self._trace('e",', (6134, 6137), self.input.position)
                _G_apply_740, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace(' ex1', (6137, 6141), self.input.position)
                _G_exactly_741, lastError = self.exactly('/')
                self.considerError(lastError, None)
                self._trace(', e', (6141, 6144), self.input.position)
                _G_apply_742, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('x2]\n        ', (6144, 6156), self.input.position)
                _G_apply_743, lastError = self._apply(self.rule_Expression6, "Expression6", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_743
                _G_python_745, lastError = eval(self._G_expr_744, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_745, self.currentError)
            def _G_or_746():
                self._trace('ession8:ex2 ', (6197, 6209), self.input.position)
                _G_apply_747, lastError = self._apply(self.rule_Expression5, "Expression5", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_747
                self._trace('"gt', (6213, 6216), self.input.position)
                _G_apply_748, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('e", ', (6216, 6220), self.input.position)
                _G_exactly_749, lastError = self.exactly('%')
                self.considerError(lastError, None)
                self._trace('ex1', (6220, 6223), self.input.position)
                _G_apply_750, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace(', ex2]\n     ', (6223, 6235), self.input.position)
                _G_apply_751, lastError = self._apply(self.rule_Expression6, "Expression6", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_751
                _G_python_753, lastError = eval(self._G_expr_752, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_753, self.currentError)
            def _G_or_754():
                self._trace(' = Expressio', (6276, 6288), self.input.position)
                _G_apply_755, lastError = self._apply(self.rule_Expression5, "Expression5", [])
                self.considerError(lastError, None)
                return (_G_apply_755, self.currentError)
            _G_or_756, lastError = self._or([_G_or_730, _G_or_738, _G_or_746, _G_or_754])
            self.considerError(lastError, 'Expression6')
            return (_G_or_756, self.currentError)


        def rule_Expression5(self):
            _locals = {'self': self}
            self.locals['Expression5'] = _locals
            def _G_or_757():
                self._trace('S Expression', (6303, 6315), self.input.position)
                _G_apply_758, lastError = self._apply(self.rule_Expression4, "Expression4", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_758
                self._trace('2 -', (6319, 6322), self.input.position)
                _G_apply_759, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('> ["', (6322, 6326), self.input.position)
                _G_exactly_760, lastError = self.exactly('^')
                self.considerError(lastError, None)
                self._trace('add', (6326, 6329), self.input.position)
                _G_apply_761, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('", ex1, ex2]', (6329, 6341), self.input.position)
                _G_apply_762, lastError = self._apply(self.rule_Expression5, "Expression5", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_762
                _G_python_764, lastError = eval(self._G_expr_763, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_764, self.currentError)
            def _G_or_765():
                self._trace("-' WS Expres", (6380, 6392), self.input.position)
                _G_apply_766, lastError = self._apply(self.rule_Expression4, "Expression4", [])
                self.considerError(lastError, None)
                return (_G_apply_766, self.currentError)
            _G_or_767, lastError = self._or([_G_or_757, _G_or_765])
            self.considerError(lastError, 'Expression5')
            return (_G_or_767, self.currentError)


        def rule_Expression4(self):
            _locals = {'self': self}
            self.locals['Expression4'] = _locals
            def _G_or_768():
                self._trace('sub"', (6407, 6411), self.input.position)
                _G_exactly_769, lastError = self.exactly('+')
                self.considerError(lastError, None)
                self._trace(', e', (6411, 6414), self.input.position)
                _G_apply_770, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('x1, ex2]\n   ', (6414, 6426), self.input.position)
                _G_apply_771, lastError = self._apply(self.rule_Expression4, "Expression4", [])
                self.considerError(lastError, None)
                return (_G_apply_771, self.currentError)
            def _G_or_772():
                self._trace(' Exp', (6440, 6444), self.input.position)
                _G_exactly_773, lastError = self.exactly('-')
                self.considerError(lastError, None)
                self._trace('res', (6444, 6447), self.input.position)
                _G_apply_774, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('sion6\n\n    E', (6447, 6459), self.input.position)
                _G_apply_775, lastError = self._apply(self.rule_Expression4, "Expression4", [])
                self.considerError(lastError, None)
                _locals['ex'] = _G_apply_775
                _G_python_777, lastError = eval(self._G_expr_776, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_777, self.currentError)
            def _G_or_778():
                self._trace("' WS Express", (6493, 6505), self.input.position)
                _G_apply_779, lastError = self._apply(self.rule_Expression3, "Expression3", [])
                self.considerError(lastError, None)
                return (_G_apply_779, self.currentError)
            _G_or_780, lastError = self._or([_G_or_768, _G_or_772, _G_or_778])
            self.considerError(lastError, 'Expression4')
            return (_G_or_780, self.currentError)


        def rule_Expression3(self):
            _locals = {'self': self}
            self.locals['Expression3'] = _locals
            def _G_or_781():
                self._trace('ulti", ex1, ', (6520, 6532), self.input.position)
                _G_apply_782, lastError = self._apply(self.rule_Expression2, "Expression2", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_782
                def _G_many1_783():
                    def _G_or_784():
                        self._trace(' | Expression5:ex1 ', (6552, 6571), self.input.position)
                        _G_apply_785, lastError = self._apply(self.rule_WS, "WS", [])
                        self.considerError(lastError, None)
                        self._trace("WS '", (6571, 6575), self.input.position)
                        _G_exactly_786, lastError = self.exactly('[')
                        self.considerError(lastError, None)
                        self._trace("/' WS Expre", (6575, 6586), self.input.position)
                        _G_apply_787, lastError = self._apply(self.rule_Expression, "Expression", [])
                        self.considerError(lastError, None)
                        _locals['prop_name'] = _G_apply_787
                        self._trace(' -> ', (6596, 6600), self.input.position)
                        _G_exactly_788, lastError = self.exactly(']')
                        self.considerError(lastError, None)
                        _G_python_790, lastError = eval(self._G_expr_789, self.globals, _locals), None
                        self.considerError(lastError, None)
                        return (_G_python_790, self.currentError)
                    def _G_or_791():
                        self._trace('x1 ', (6651, 6654), self.input.position)
                        _G_apply_792, lastError = self._apply(self.rule_WS, "WS", [])
                        self.considerError(lastError, None)
                        self._trace("WS '", (6654, 6658), self.input.position)
                        _G_exactly_793, lastError = self.exactly('[')
                        self.considerError(lastError, None)
                        def _G_optional_794():
                            self._trace("%' WS Expre", (6658, 6669), self.input.position)
                            _G_apply_795, lastError = self._apply(self.rule_Expression, "Expression", [])
                            self.considerError(lastError, None)
                            return (_G_apply_795, self.currentError)
                        def _G_optional_796():
                            return (None, self.input.nullError())
                        _G_or_797, lastError = self._or([_G_optional_794, _G_optional_796])
                        self.considerError(lastError, None)
                        _locals['start'] = _G_or_797
                        self._trace('ex2 -', (6676, 6681), self.input.position)
                        _G_exactly_798, lastError = self.exactly('..')
                        self.considerError(lastError, None)
                        def _G_optional_799():
                            self._trace('> ["mod",  ', (6681, 6692), self.input.position)
                            _G_apply_800, lastError = self._apply(self.rule_Expression, "Expression", [])
                            self.considerError(lastError, None)
                            return (_G_apply_800, self.currentError)
                        def _G_optional_801():
                            return (None, self.input.nullError())
                        _G_or_802, lastError = self._or([_G_optional_799, _G_optional_801])
                        self.considerError(lastError, None)
                        _locals['end'] = _G_or_802
                        self._trace(' ex2', (6697, 6701), self.input.position)
                        _G_exactly_803, lastError = self.exactly(']')
                        self.considerError(lastError, None)
                        _G_python_805, lastError = eval(self._G_expr_804, self.globals, _locals), None
                        self.considerError(lastError, None)
                        return (_G_python_805, self.currentError)
                    def _G_or_806():
                        def _G_or_807():
                            self._trace('on5 = Expression4:ex1 W', (6746, 6769), self.input.position)
                            _G_apply_808, lastError = self._apply(self.rule_WS, "WS", [])
                            self.considerError(lastError, None)
                            self._trace("S '^'", (6769, 6774), self.input.position)
                            _G_exactly_809, lastError = self.exactly('=~')
                            self.considerError(lastError, None)
                            _G_python_810, lastError = ("regex"), None
                            self.considerError(lastError, None)
                            return (_G_python_810, self.currentError)
                        def _G_or_811():
                            self._trace('1, ', (6807, 6810), self.input.position)
                            _G_apply_812, lastError = self._apply(self.rule_SP, "SP", [])
                            self.considerError(lastError, None)
                            self._trace('ex', (6810, 6812), self.input.position)
                            _G_apply_813, lastError = self._apply(self.rule_I, "I", [])
                            self.considerError(lastError, None)
                            self._trace('2]', (6812, 6814), self.input.position)
                            _G_apply_814, lastError = self._apply(self.rule_N, "N", [])
                            self.considerError(lastError, None)
                            _G_python_815, lastError = ("in"), None
                            self.considerError(lastError, None)
                            return (_G_python_815, self.currentError)
                        def _G_or_816():
                            self._trace('\n\n ', (6844, 6847), self.input.position)
                            _G_apply_817, lastError = self._apply(self.rule_SP, "SP", [])
                            self.considerError(lastError, None)
                            self._trace('  ', (6847, 6849), self.input.position)
                            _G_apply_818, lastError = self._apply(self.rule_S, "S", [])
                            self.considerError(lastError, None)
                            self._trace(' E', (6849, 6851), self.input.position)
                            _G_apply_819, lastError = self._apply(self.rule_T, "T", [])
                            self.considerError(lastError, None)
                            self._trace('xp', (6851, 6853), self.input.position)
                            _G_apply_820, lastError = self._apply(self.rule_A, "A", [])
                            self.considerError(lastError, None)
                            self._trace('re', (6853, 6855), self.input.position)
                            _G_apply_821, lastError = self._apply(self.rule_R, "R", [])
                            self.considerError(lastError, None)
                            self._trace('ss', (6855, 6857), self.input.position)
                            _G_apply_822, lastError = self._apply(self.rule_T, "T", [])
                            self.considerError(lastError, None)
                            self._trace('io', (6857, 6859), self.input.position)
                            _G_apply_823, lastError = self._apply(self.rule_S, "S", [])
                            self.considerError(lastError, None)
                            self._trace('n4 ', (6859, 6862), self.input.position)
                            _G_apply_824, lastError = self._apply(self.rule_SP, "SP", [])
                            self.considerError(lastError, None)
                            self._trace('= ', (6862, 6864), self.input.position)
                            _G_apply_825, lastError = self._apply(self.rule_W, "W", [])
                            self.considerError(lastError, None)
                            self._trace("'+", (6864, 6866), self.input.position)
                            _G_apply_826, lastError = self._apply(self.rule_I, "I", [])
                            self.considerError(lastError, None)
                            self._trace("' ", (6866, 6868), self.input.position)
                            _G_apply_827, lastError = self._apply(self.rule_T, "T", [])
                            self.considerError(lastError, None)
                            self._trace('WS', (6868, 6870), self.input.position)
                            _G_apply_828, lastError = self._apply(self.rule_H, "H", [])
                            self.considerError(lastError, None)
                            _G_python_829, lastError = ("starts_with"), None
                            self.considerError(lastError, None)
                            return (_G_python_829, self.currentError)
                        def _G_or_830():
                            self._trace('xpr', (6909, 6912), self.input.position)
                            _G_apply_831, lastError = self._apply(self.rule_SP, "SP", [])
                            self.considerError(lastError, None)
                            self._trace('es', (6912, 6914), self.input.position)
                            _G_apply_832, lastError = self._apply(self.rule_E, "E", [])
                            self.considerError(lastError, None)
                            self._trace('si', (6914, 6916), self.input.position)
                            _G_apply_833, lastError = self._apply(self.rule_N, "N", [])
                            self.considerError(lastError, None)
                            self._trace('on', (6916, 6918), self.input.position)
                            _G_apply_834, lastError = self._apply(self.rule_D, "D", [])
                            self.considerError(lastError, None)
                            self._trace('4:', (6918, 6920), self.input.position)
                            _G_apply_835, lastError = self._apply(self.rule_S, "S", [])
                            self.considerError(lastError, None)
                            self._trace('ex ', (6920, 6923), self.input.position)
                            _G_apply_836, lastError = self._apply(self.rule_SP, "SP", [])
                            self.considerError(lastError, None)
                            self._trace('->', (6923, 6925), self.input.position)
                            _G_apply_837, lastError = self._apply(self.rule_W, "W", [])
                            self.considerError(lastError, None)
                            self._trace(' [', (6925, 6927), self.input.position)
                            _G_apply_838, lastError = self._apply(self.rule_I, "I", [])
                            self.considerError(lastError, None)
                            self._trace('"m', (6927, 6929), self.input.position)
                            _G_apply_839, lastError = self._apply(self.rule_T, "T", [])
                            self.considerError(lastError, None)
                            self._trace('in', (6929, 6931), self.input.position)
                            _G_apply_840, lastError = self._apply(self.rule_H, "H", [])
                            self.considerError(lastError, None)
                            _G_python_841, lastError = ("ends_with"), None
                            self.considerError(lastError, None)
                            return (_G_python_841, self.currentError)
                        def _G_or_842():
                            self._trace('\n\n ', (6969, 6972), self.input.position)
                            _G_apply_843, lastError = self._apply(self.rule_SP, "SP", [])
                            self.considerError(lastError, None)
                            self._trace('  ', (6972, 6974), self.input.position)
                            _G_apply_844, lastError = self._apply(self.rule_C, "C", [])
                            self.considerError(lastError, None)
                            self._trace(' E', (6974, 6976), self.input.position)
                            _G_apply_845, lastError = self._apply(self.rule_O, "O", [])
                            self.considerError(lastError, None)
                            self._trace('xp', (6976, 6978), self.input.position)
                            _G_apply_846, lastError = self._apply(self.rule_N, "N", [])
                            self.considerError(lastError, None)
                            self._trace('re', (6978, 6980), self.input.position)
                            _G_apply_847, lastError = self._apply(self.rule_T, "T", [])
                            self.considerError(lastError, None)
                            self._trace('ss', (6980, 6982), self.input.position)
                            _G_apply_848, lastError = self._apply(self.rule_A, "A", [])
                            self.considerError(lastError, None)
                            self._trace('io', (6982, 6984), self.input.position)
                            _G_apply_849, lastError = self._apply(self.rule_I, "I", [])
                            self.considerError(lastError, None)
                            self._trace('n3', (6984, 6986), self.input.position)
                            _G_apply_850, lastError = self._apply(self.rule_N, "N", [])
                            self.considerError(lastError, None)
                            self._trace(' =', (6986, 6988), self.input.position)
                            _G_apply_851, lastError = self._apply(self.rule_S, "S", [])
                            self.considerError(lastError, None)
                            _G_python_852, lastError = ("contains"), None
                            self.considerError(lastError, None)
                            return (_G_python_852, self.currentError)
                        _G_or_853, lastError = self._or([_G_or_807, _G_or_811, _G_or_816, _G_or_830, _G_or_842])
                        self.considerError(lastError, None)
                        _locals['operator'] = _G_or_853
                        self._trace('   ', (7030, 7033), self.input.position)
                        _G_apply_854, lastError = self._apply(self.rule_WS, "WS", [])
                        self.considerError(lastError, None)
                        self._trace('            ', (7033, 7045), self.input.position)
                        _G_apply_855, lastError = self._apply(self.rule_Expression2, "Expression2", [])
                        self.considerError(lastError, None)
                        _locals['ex2'] = _G_apply_855
                        _G_python_857, lastError = eval(self._G_expr_856, self.globals, _locals), None
                        self.considerError(lastError, None)
                        return (_G_python_857, self.currentError)
                    def _G_or_858():
                        self._trace('ert', (7086, 7089), self.input.position)
                        _G_apply_859, lastError = self._apply(self.rule_SP, "SP", [])
                        self.considerError(lastError, None)
                        self._trace('yL', (7089, 7091), self.input.position)
                        _G_apply_860, lastError = self._apply(self.rule_I, "I", [])
                        self.considerError(lastError, None)
                        self._trace('oo', (7091, 7093), self.input.position)
                        _G_apply_861, lastError = self._apply(self.rule_S, "S", [])
                        self.considerError(lastError, None)
                        self._trace('kup', (7093, 7096), self.input.position)
                        _G_apply_862, lastError = self._apply(self.rule_SP, "SP", [])
                        self.considerError(lastError, None)
                        self._trace('",', (7096, 7098), self.input.position)
                        _G_apply_863, lastError = self._apply(self.rule_N, "N", [])
                        self.considerError(lastError, None)
                        self._trace(' p', (7098, 7100), self.input.position)
                        _G_apply_864, lastError = self._apply(self.rule_U, "U", [])
                        self.considerError(lastError, None)
                        self._trace('ro', (7100, 7102), self.input.position)
                        _G_apply_865, lastError = self._apply(self.rule_L, "L", [])
                        self.considerError(lastError, None)
                        self._trace('p_', (7102, 7104), self.input.position)
                        _G_apply_866, lastError = self._apply(self.rule_L, "L", [])
                        self.considerError(lastError, None)
                        _G_python_867, lastError = (["is_null"]), None
                        self.considerError(lastError, None)
                        return (_G_python_867, self.currentError)
                    def _G_or_868():
                        self._trace(' Ex', (7138, 7141), self.input.position)
                        _G_apply_869, lastError = self._apply(self.rule_SP, "SP", [])
                        self.considerError(lastError, None)
                        self._trace('pr', (7141, 7143), self.input.position)
                        _G_apply_870, lastError = self._apply(self.rule_I, "I", [])
                        self.considerError(lastError, None)
                        self._trace('es', (7143, 7145), self.input.position)
                        _G_apply_871, lastError = self._apply(self.rule_S, "S", [])
                        self.considerError(lastError, None)
                        self._trace('sio', (7145, 7148), self.input.position)
                        _G_apply_872, lastError = self._apply(self.rule_SP, "SP", [])
                        self.considerError(lastError, None)
                        self._trace('n?', (7148, 7150), self.input.position)
                        _G_apply_873, lastError = self._apply(self.rule_N, "N", [])
                        self.considerError(lastError, None)
                        self._trace(':s', (7150, 7152), self.input.position)
                        _G_apply_874, lastError = self._apply(self.rule_O, "O", [])
                        self.considerError(lastError, None)
                        self._trace('ta', (7152, 7154), self.input.position)
                        _G_apply_875, lastError = self._apply(self.rule_T, "T", [])
                        self.considerError(lastError, None)
                        self._trace('rt ', (7154, 7157), self.input.position)
                        _G_apply_876, lastError = self._apply(self.rule_SP, "SP", [])
                        self.considerError(lastError, None)
                        self._trace("'.", (7157, 7159), self.input.position)
                        _G_apply_877, lastError = self._apply(self.rule_N, "N", [])
                        self.considerError(lastError, None)
                        self._trace(".'", (7159, 7161), self.input.position)
                        _G_apply_878, lastError = self._apply(self.rule_U, "U", [])
                        self.considerError(lastError, None)
                        self._trace(' E', (7161, 7163), self.input.position)
                        _G_apply_879, lastError = self._apply(self.rule_L, "L", [])
                        self.considerError(lastError, None)
                        self._trace('xp', (7163, 7165), self.input.position)
                        _G_apply_880, lastError = self._apply(self.rule_L, "L", [])
                        self.considerError(lastError, None)
                        _G_python_881, lastError = (["is_not_null"]), None
                        self.considerError(lastError, None)
                        return (_G_python_881, self.currentError)
                    _G_or_882, lastError = self._or([_G_or_784, _G_or_791, _G_or_806, _G_or_858, _G_or_868])
                    self.considerError(lastError, None)
                    return (_G_or_882, self.currentError)
                _G_many1_883, lastError = self.many(_G_many1_783, _G_many1_783())
                self.considerError(lastError, None)
                _locals['c'] = _G_many1_883
                _G_python_885, lastError = eval(self._G_expr_884, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_885, self.currentError)
            def _G_or_886():
                self._trace('         WS ', (7246, 7258), self.input.position)
                _G_apply_887, lastError = self._apply(self.rule_Expression2, "Expression2", [])
                self.considerError(lastError, None)
                return (_G_apply_887, self.currentError)
            _G_or_888, lastError = self._or([_G_or_781, _G_or_886])
            self.considerError(lastError, 'Expression3')
            return (_G_or_888, self.currentError)


        def rule_Expression2(self):
            _locals = {'self': self}
            self.locals['Expression2'] = _locals
            def _G_or_889():
                self._trace('\n    ', (7273, 7278), self.input.position)
                _G_apply_890, lastError = self._apply(self.rule_Atom, "Atom", [])
                self.considerError(lastError, None)
                _locals['a'] = _G_apply_890
                def _G_many1_891():
                    def _G_or_892():
                        self._trace('              ', (7282, 7296), self.input.position)
                        _G_apply_893, lastError = self._apply(self.rule_PropertyLookup, "PropertyLookup", [])
                        self.considerError(lastError, None)
                        return (_G_apply_893, self.currentError)
                    def _G_or_894():
                        self._trace('| SP I N ->', (7298, 7309), self.input.position)
                        _G_apply_895, lastError = self._apply(self.rule_NodeLabels, "NodeLabels", [])
                        self.considerError(lastError, None)
                        return (_G_apply_895, self.currentError)
                    _G_or_896, lastError = self._or([_G_or_892, _G_or_894])
                    self.considerError(lastError, None)
                    return (_G_or_896, self.currentError)
                _G_many1_897, lastError = self.many(_G_many1_891, _G_many1_891())
                self.considerError(lastError, None)
                _locals['c'] = _G_many1_897
                _G_python_899, lastError = eval(self._G_expr_898, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_899, self.currentError)
            def _G_or_900():
                self._trace('S SP ', (7354, 7359), self.input.position)
                _G_apply_901, lastError = self._apply(self.rule_Atom, "Atom", [])
                self.considerError(lastError, None)
                return (_G_apply_901, self.currentError)
            _G_or_902, lastError = self._or([_G_or_889, _G_or_900])
            self.considerError(lastError, 'Expression2')
            return (_G_or_902, self.currentError)


        def rule_Atom(self):
            _locals = {'self': self}
            self.locals['Atom'] = _locals
            def _G_or_903():
                self._trace('-> "starts_wit', (7367, 7381), self.input.position)
                _G_apply_904, lastError = self._apply(self.rule_NumberLiteral, "NumberLiteral", [])
                self.considerError(lastError, None)
                return (_G_apply_904, self.currentError)
            def _G_or_905():
                self._trace('              ', (7388, 7402), self.input.position)
                _G_apply_906, lastError = self._apply(self.rule_StringLiteral, "StringLiteral", [])
                self.considerError(lastError, None)
                return (_G_apply_906, self.currentError)
            def _G_or_907():
                self._trace(' SP E N D ', (7409, 7419), self.input.position)
                _G_apply_908, lastError = self._apply(self.rule_Parameter, "Parameter", [])
                self.considerError(lastError, None)
                return (_G_apply_908, self.currentError)
            def _G_or_909():
                self._trace('I ', (7426, 7428), self.input.position)
                _G_apply_910, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                self._trace('T ', (7428, 7430), self.input.position)
                _G_apply_911, lastError = self._apply(self.rule_R, "R", [])
                self.considerError(lastError, None)
                self._trace('H ', (7430, 7432), self.input.position)
                _G_apply_912, lastError = self._apply(self.rule_U, "U", [])
                self.considerError(lastError, None)
                self._trace(' -', (7432, 7434), self.input.position)
                _G_apply_913, lastError = self._apply(self.rule_E, "E", [])
                self.considerError(lastError, None)
                _G_python_914, lastError = (["Literal", True]), None
                self.considerError(lastError, None)
                return (_G_python_914, self.currentError)
            def _G_or_915():
                self._trace('  ', (7462, 7464), self.input.position)
                _G_apply_916, lastError = self._apply(self.rule_F, "F", [])
                self.considerError(lastError, None)
                self._trace('  ', (7464, 7466), self.input.position)
                _G_apply_917, lastError = self._apply(self.rule_A, "A", [])
                self.considerError(lastError, None)
                self._trace('  ', (7466, 7468), self.input.position)
                _G_apply_918, lastError = self._apply(self.rule_L, "L", [])
                self.considerError(lastError, None)
                self._trace('  ', (7468, 7470), self.input.position)
                _G_apply_919, lastError = self._apply(self.rule_S, "S", [])
                self.considerError(lastError, None)
                self._trace('  ', (7470, 7472), self.input.position)
                _G_apply_920, lastError = self._apply(self.rule_E, "E", [])
                self.considerError(lastError, None)
                _G_python_921, lastError = (["Literal", False]), None
                self.considerError(lastError, None)
                return (_G_python_921, self.currentError)
            def _G_or_922():
                self._trace('ta', (7501, 7503), self.input.position)
                _G_apply_923, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace('in', (7503, 7505), self.input.position)
                _G_apply_924, lastError = self._apply(self.rule_U, "U", [])
                self.considerError(lastError, None)
                self._trace('s"', (7505, 7507), self.input.position)
                _G_apply_925, lastError = self._apply(self.rule_L, "L", [])
                self.considerError(lastError, None)
                self._trace('\n ', (7507, 7509), self.input.position)
                _G_apply_926, lastError = self._apply(self.rule_L, "L", [])
                self.considerError(lastError, None)
                _G_python_927, lastError = (["Literal", None]), None
                self.considerError(lastError, None)
                return (_G_python_927, self.currentError)
            def _G_or_928():
                self._trace('r WS Expression', (7537, 7552), self.input.position)
                _G_apply_929, lastError = self._apply(self.rule_CaseExpression, "CaseExpression", [])
                self.considerError(lastError, None)
                return (_G_apply_929, self.currentError)
            def _G_or_930():
                self._trace('> ', (7559, 7561), self.input.position)
                _G_apply_931, lastError = self._apply(self.rule_C, "C", [])
                self.considerError(lastError, None)
                self._trace('[o', (7561, 7563), self.input.position)
                _G_apply_932, lastError = self._apply(self.rule_O, "O", [])
                self.considerError(lastError, None)
                self._trace('pe', (7563, 7565), self.input.position)
                _G_apply_933, lastError = self._apply(self.rule_U, "U", [])
                self.considerError(lastError, None)
                self._trace('ra', (7565, 7567), self.input.position)
                _G_apply_934, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace('to', (7567, 7569), self.input.position)
                _G_apply_935, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                self._trace('r, e', (7569, 7573), self.input.position)
                _G_exactly_936, lastError = self.exactly('(')
                self.considerError(lastError, None)
                self._trace('x2]\n', (7573, 7577), self.input.position)
                _G_exactly_937, lastError = self.exactly('*')
                self.considerError(lastError, None)
                self._trace('    ', (7577, 7581), self.input.position)
                _G_exactly_938, lastError = self.exactly(')')
                self.considerError(lastError, None)
                _G_python_939, lastError = (["count *"]), None
                self.considerError(lastError, None)
                return (_G_python_939, self.currentError)
            def _G_or_940():
                self._trace(' S SP N U L', (7603, 7614), self.input.position)
                _G_apply_941, lastError = self._apply(self.rule_MapLiteral, "MapLiteral", [])
                self.considerError(lastError, None)
                return (_G_apply_941, self.currentError)
            def _G_or_942():
                self._trace('["is_null"]\n      ', (7621, 7639), self.input.position)
                _G_apply_943, lastError = self._apply(self.rule_ListComprehension, "ListComprehension", [])
                self.considerError(lastError, None)
                return (_G_apply_943, self.currentError)
            def _G_or_944():
                self._trace('    ', (7646, 7650), self.input.position)
                _G_exactly_945, lastError = self.exactly('[')
                self.considerError(lastError, None)
                def _G_or_946():
                    self._trace(' N O T SP N U L L -', (7664, 7683), self.input.position)
                    _G_apply_947, lastError = self._apply(self.rule_WS, "WS", [])
                    self.considerError(lastError, None)
                    self._trace('> ["is_not_', (7683, 7694), self.input.position)
                    _G_apply_948, lastError = self._apply(self.rule_Expression, "Expression", [])
                    self.considerError(lastError, None)
                    _locals['head'] = _G_apply_948
                    self._trace(']\n ', (7699, 7702), self.input.position)
                    _G_apply_949, lastError = self._apply(self.rule_WS, "WS", [])
                    self.considerError(lastError, None)
                    def _G_many_950():
                        self._trace('+:c', (7720, 7723), self.input.position)
                        _G_exactly_951, lastError = self.exactly(',')
                        self.considerError(lastError, None)
                        self._trace(' ->', (7723, 7726), self.input.position)
                        _G_apply_952, lastError = self._apply(self.rule_WS, "WS", [])
                        self.considerError(lastError, None)
                        self._trace(' ["Expressi', (7726, 7737), self.input.position)
                        _G_apply_953, lastError = self._apply(self.rule_Expression, "Expression", [])
                        self.considerError(lastError, None)
                        _locals['item'] = _G_apply_953
                        self._trace(' ex', (7742, 7745), self.input.position)
                        _G_apply_954, lastError = self._apply(self.rule_WS, "WS", [])
                        self.considerError(lastError, None)
                        _G_python_956, lastError = eval(self._G_expr_955, self.globals, _locals), None
                        self.considerError(lastError, None)
                        return (_G_python_956, self.currentError)
                    _G_many_957, lastError = self.many(_G_many_950)
                    self.considerError(lastError, None)
                    _locals['tail'] = _G_many_957
                    _G_python_958, lastError = eval(self._G_expr_443, self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_958, self.currentError)
                def _G_or_959():
                    _G_python_960, lastError = ([]), None
                    self.considerError(lastError, None)
                    return (_G_python_960, self.currentError)
                _G_or_961, lastError = self._or([_G_or_946, _G_or_959])
                self.considerError(lastError, None)
                _locals['ex'] = _G_or_961
                self._trace('ession2", a,', (7851, 7863), self.input.position)
                _G_exactly_962, lastError = self.exactly(']')
                self.considerError(lastError, None)
                _G_python_964, lastError = eval(self._G_expr_963, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_964, self.currentError)
            def _G_or_965():
                self._trace(' A', (7886, 7888), self.input.position)
                _G_apply_966, lastError = self._apply(self.rule_F, "F", [])
                self.considerError(lastError, None)
                self._trace('to', (7888, 7890), self.input.position)
                _G_apply_967, lastError = self._apply(self.rule_I, "I", [])
                self.considerError(lastError, None)
                self._trace('m\n', (7890, 7892), self.input.position)
                _G_apply_968, lastError = self._apply(self.rule_L, "L", [])
                self.considerError(lastError, None)
                self._trace('\n ', (7892, 7894), self.input.position)
                _G_apply_969, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                self._trace('  ', (7894, 7896), self.input.position)
                _G_apply_970, lastError = self._apply(self.rule_E, "E", [])
                self.considerError(lastError, None)
                self._trace(' A', (7896, 7898), self.input.position)
                _G_apply_971, lastError = self._apply(self.rule_R, "R", [])
                self.considerError(lastError, None)
                self._trace('tom', (7898, 7901), self.input.position)
                _G_apply_972, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace(' = N', (7901, 7905), self.input.position)
                _G_exactly_973, lastError = self.exactly('(')
                self.considerError(lastError, None)
                self._trace('umb', (7905, 7908), self.input.position)
                _G_apply_974, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('erLiteral\n       ', (7908, 7925), self.input.position)
                _G_apply_975, lastError = self._apply(self.rule_FilterExpression, "FilterExpression", [])
                self.considerError(lastError, None)
                _locals['fex'] = _G_apply_975
                self._trace('Str', (7929, 7932), self.input.position)
                _G_apply_976, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('ingL', (7932, 7936), self.input.position)
                _G_exactly_977, lastError = self.exactly(')')
                self.considerError(lastError, None)
                _G_python_979, lastError = eval(self._G_expr_978, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_979, self.currentError)
            def _G_or_980():
                self._trace('r\n', (7962, 7964), self.input.position)
                _G_apply_981, lastError = self._apply(self.rule_E, "E", [])
                self.considerError(lastError, None)
                self._trace('  ', (7964, 7966), self.input.position)
                _G_apply_982, lastError = self._apply(self.rule_X, "X", [])
                self.considerError(lastError, None)
                self._trace('  ', (7966, 7968), self.input.position)
                _G_apply_983, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                self._trace('  ', (7968, 7970), self.input.position)
                _G_apply_984, lastError = self._apply(self.rule_R, "R", [])
                self.considerError(lastError, None)
                self._trace('  ', (7970, 7972), self.input.position)
                _G_apply_985, lastError = self._apply(self.rule_A, "A", [])
                self.considerError(lastError, None)
                self._trace(' |', (7972, 7974), self.input.position)
                _G_apply_986, lastError = self._apply(self.rule_C, "C", [])
                self.considerError(lastError, None)
                self._trace(' T', (7974, 7976), self.input.position)
                _G_apply_987, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                self._trace(' R ', (7976, 7979), self.input.position)
                _G_apply_988, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('U E ', (7979, 7983), self.input.position)
                _G_exactly_989, lastError = self.exactly('(')
                self.considerError(lastError, None)
                self._trace('-> ', (7983, 7986), self.input.position)
                _G_apply_990, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('["Literal", True]', (7986, 8003), self.input.position)
                _G_apply_991, lastError = self._apply(self.rule_FilterExpression, "FilterExpression", [])
                self.considerError(lastError, None)
                _locals['fex'] = _G_apply_991
                self._trace('   ', (8007, 8010), self.input.position)
                _G_apply_992, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                def _G_optional_993():
                    self._trace(' |', (8012, 8014), self.input.position)
                    _G_apply_994, lastError = self._apply(self.rule_WS, "WS", [])
                    self.considerError(lastError, None)
                    self._trace(' F A', (8014, 8018), self.input.position)
                    _G_exactly_995, lastError = self.exactly('|')
                    self.considerError(lastError, None)
                    self._trace(' L S E -> [', (8018, 8029), self.input.position)
                    _G_apply_996, lastError = self._apply(self.rule_Expression, "Expression", [])
                    self.considerError(lastError, None)
                    return (_G_apply_996, self.currentError)
                def _G_optional_997():
                    return (None, self.input.nullError())
                _G_or_998, lastError = self._or([_G_optional_993, _G_optional_997])
                self.considerError(lastError, None)
                _locals['ex'] = _G_or_998
                self._trace('ral"', (8034, 8038), self.input.position)
                _G_exactly_999, lastError = self.exactly(')')
                self.considerError(lastError, None)
                _G_python_1001, lastError = eval(self._G_expr_1000, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_1001, self.currentError)
            def _G_or_1002():
                self._trace('["', (8069, 8071), self.input.position)
                _G_apply_1003, lastError = self._apply(self.rule_A, "A", [])
                self.considerError(lastError, None)
                self._trace('Li', (8071, 8073), self.input.position)
                _G_apply_1004, lastError = self._apply(self.rule_L, "L", [])
                self.considerError(lastError, None)
                self._trace('te', (8073, 8075), self.input.position)
                _G_apply_1005, lastError = self._apply(self.rule_L, "L", [])
                self.considerError(lastError, None)
                self._trace('ral', (8075, 8078), self.input.position)
                _G_apply_1006, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('", N', (8078, 8082), self.input.position)
                _G_exactly_1007, lastError = self.exactly('(')
                self.considerError(lastError, None)
                self._trace('one', (8082, 8085), self.input.position)
                _G_apply_1008, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace(']\n         | Case', (8085, 8102), self.input.position)
                _G_apply_1009, lastError = self._apply(self.rule_FilterExpression, "FilterExpression", [])
                self.considerError(lastError, None)
                _locals['fex'] = _G_apply_1009
                self._trace('ess', (8106, 8109), self.input.position)
                _G_apply_1010, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('ion\n', (8109, 8113), self.input.position)
                _G_exactly_1011, lastError = self.exactly(')')
                self.considerError(lastError, None)
                _G_python_1013, lastError = eval(self._G_expr_1012, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_1013, self.currentError)
            def _G_or_1014():
                self._trace("' ", (8136, 8138), self.input.position)
                _G_apply_1015, lastError = self._apply(self.rule_A, "A", [])
                self.considerError(lastError, None)
                self._trace("'*", (8138, 8140), self.input.position)
                _G_apply_1016, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace("' ", (8140, 8142), self.input.position)
                _G_apply_1017, lastError = self._apply(self.rule_Y, "Y", [])
                self.considerError(lastError, None)
                self._trace("')'", (8142, 8145), self.input.position)
                _G_apply_1018, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace(' -> ', (8145, 8149), self.input.position)
                _G_exactly_1019, lastError = self.exactly('(')
                self.considerError(lastError, None)
                self._trace('["c', (8149, 8152), self.input.position)
                _G_apply_1020, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('ount *"]\n        ', (8152, 8169), self.input.position)
                _G_apply_1021, lastError = self._apply(self.rule_FilterExpression, "FilterExpression", [])
                self.considerError(lastError, None)
                _locals['fex'] = _G_apply_1021
                self._trace('apL', (8173, 8176), self.input.position)
                _G_apply_1022, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('iter', (8176, 8180), self.input.position)
                _G_exactly_1023, lastError = self.exactly(')')
                self.considerError(lastError, None)
                _G_python_1025, lastError = eval(self._G_expr_1024, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_1025, self.currentError)
            def _G_or_1026():
                self._trace('eh', (8203, 8205), self.input.position)
                _G_apply_1027, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace('en', (8205, 8207), self.input.position)
                _G_apply_1028, lastError = self._apply(self.rule_O, "O", [])
                self.considerError(lastError, None)
                self._trace('si', (8207, 8209), self.input.position)
                _G_apply_1029, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace('on', (8209, 8211), self.input.position)
                _G_apply_1030, lastError = self._apply(self.rule_E, "E", [])
                self.considerError(lastError, None)
                self._trace('\n  ', (8211, 8214), self.input.position)
                _G_apply_1031, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('    ', (8214, 8218), self.input.position)
                _G_exactly_1032, lastError = self.exactly('(')
                self.considerError(lastError, None)
                self._trace('   ', (8218, 8221), self.input.position)
                _G_apply_1033, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace("| '['\n           ", (8221, 8238), self.input.position)
                _G_apply_1034, lastError = self._apply(self.rule_FilterExpression, "FilterExpression", [])
                self.considerError(lastError, None)
                _locals['fex'] = _G_apply_1034
                self._trace(' (\n', (8242, 8245), self.input.position)
                _G_apply_1035, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('    ', (8245, 8249), self.input.position)
                _G_exactly_1036, lastError = self.exactly(')')
                self.considerError(lastError, None)
                _G_python_1038, lastError = eval(self._G_expr_1037, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_1038, self.currentError)
            def _G_or_1039():
                self._trace('ss', (8273, 8275), self.input.position)
                _G_apply_1040, lastError = self._apply(self.rule_S, "S", [])
                self.considerError(lastError, None)
                self._trace('io', (8275, 8277), self.input.position)
                _G_apply_1041, lastError = self._apply(self.rule_I, "I", [])
                self.considerError(lastError, None)
                self._trace('n:', (8277, 8279), self.input.position)
                _G_apply_1042, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace('he', (8279, 8281), self.input.position)
                _G_apply_1043, lastError = self._apply(self.rule_G, "G", [])
                self.considerError(lastError, None)
                self._trace('ad', (8281, 8283), self.input.position)
                _G_apply_1044, lastError = self._apply(self.rule_L, "L", [])
                self.considerError(lastError, None)
                self._trace(' W', (8283, 8285), self.input.position)
                _G_apply_1045, lastError = self._apply(self.rule_E, "E", [])
                self.considerError(lastError, None)
                self._trace('S\n ', (8285, 8288), self.input.position)
                _G_apply_1046, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('    ', (8288, 8292), self.input.position)
                _G_exactly_1047, lastError = self.exactly('(')
                self.considerError(lastError, None)
                self._trace('   ', (8292, 8295), self.input.position)
                _G_apply_1048, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace("            (',' ", (8295, 8312), self.input.position)
                _G_apply_1049, lastError = self._apply(self.rule_FilterExpression, "FilterExpression", [])
                self.considerError(lastError, None)
                _locals['fex'] = _G_apply_1049
                self._trace('xpr', (8316, 8319), self.input.position)
                _G_apply_1050, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('essi', (8319, 8323), self.input.position)
                _G_exactly_1051, lastError = self.exactly(')')
                self.considerError(lastError, None)
                _G_python_1053, lastError = eval(self._G_expr_1052, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_1053, self.currentError)
            def _G_or_1054():
                self._trace('             )*:tail ', (8349, 8370), self.input.position)
                _G_apply_1055, lastError = self._apply(self.rule_RelationshipsPattern, "RelationshipsPattern", [])
                self.considerError(lastError, None)
                return (_G_apply_1055, self.currentError)
            def _G_or_1056():
                self._trace('d] + tail\n                ', (8377, 8403), self.input.position)
                _G_apply_1057, lastError = self._apply(self.rule_GraphRelationshipsPattern, "GraphRelationshipsPattern", [])
                self.considerError(lastError, None)
                return (_G_apply_1057, self.currentError)
            def _G_or_1058():
                self._trace('                   -> []\n', (8410, 8435), self.input.position)
                _G_apply_1059, lastError = self._apply(self.rule_ExplicitExistsExpression, "ExplicitExistsExpression", [])
                self.considerError(lastError, None)
                return (_G_apply_1059, self.currentError)
            def _G_or_1060():
                self._trace('         ):ex\n ', (8442, 8457), self.input.position)
                _G_apply_1061, lastError = self._apply(self.rule_ExistsFunction, "ExistsFunction", [])
                self.considerError(lastError, None)
                return (_G_apply_1061, self.currentError)
            def _G_or_1062():
                self._trace('    \']\' -> ["List", ex]\n', (8464, 8488), self.input.position)
                _G_apply_1063, lastError = self._apply(self.rule_parenthesizedExpression, "parenthesizedExpression", [])
                self.considerError(lastError, None)
                return (_G_apply_1063, self.currentError)
            def _G_or_1064():
                self._trace('  | F I L T E R WS ', (8495, 8514), self.input.position)
                _G_apply_1065, lastError = self._apply(self.rule_FunctionInvocation, "FunctionInvocation", [])
                self.considerError(lastError, None)
                return (_G_apply_1065, self.currentError)
            def _G_or_1066():
                self._trace('FilterExp', (8521, 8530), self.input.position)
                _G_apply_1067, lastError = self._apply(self.rule_Variable, "Variable", [])
                self.considerError(lastError, None)
                return (_G_apply_1067, self.currentError)
            _G_or_1068, lastError = self._or([_G_or_903, _G_or_905, _G_or_907, _G_or_909, _G_or_915, _G_or_922, _G_or_928, _G_or_930, _G_or_940, _G_or_942, _G_or_944, _G_or_965, _G_or_980, _G_or_1002, _G_or_1014, _G_or_1026, _G_or_1039, _G_or_1054, _G_or_1056, _G_or_1058, _G_or_1060, _G_or_1062, _G_or_1064, _G_or_1066])
            self.considerError(lastError, 'Atom')
            return (_G_or_1068, self.currentError)


        def rule_parenthesizedExpression(self):
            _locals = {'self': self}
            self.locals['parenthesizedExpression'] = _locals
            self._trace('ter"', (8557, 8561), self.input.position)
            _G_exactly_1069, lastError = self.exactly('(')
            self.considerError(lastError, 'parenthesizedExpression')
            self._trace(', f', (8561, 8564), self.input.position)
            _G_apply_1070, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'parenthesizedExpression')
            self._trace('ex]\n       ', (8564, 8575), self.input.position)
            _G_apply_1071, lastError = self._apply(self.rule_Expression, "Expression", [])
            self.considerError(lastError, 'parenthesizedExpression')
            _locals['ex'] = _G_apply_1071
            self._trace(' E ', (8578, 8581), self.input.position)
            _G_apply_1072, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'parenthesizedExpression')
            self._trace('X T ', (8581, 8585), self.input.position)
            _G_exactly_1073, lastError = self.exactly(')')
            self.considerError(lastError, 'parenthesizedExpression')
            _G_python_1075, lastError = eval(self._G_expr_1074, self.globals, _locals), None
            self.considerError(lastError, 'parenthesizedExpression')
            return (_G_python_1075, self.currentError)


        def rule_RelationshipsPattern(self):
            _locals = {'self': self}
            self.locals['RelationshipsPattern'] = _locals
            self._trace('sion:fex WS ', (8615, 8627), self.input.position)
            _G_apply_1076, lastError = self._apply(self.rule_NodePattern, "NodePattern", [])
            self.considerError(lastError, 'RelationshipsPattern')
            _locals['np'] = _G_apply_1076
            def _G_many_1077():
                self._trace("|'", (8632, 8634), self.input.position)
                _G_apply_1078, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace(" Expression)?:ex ')'", (8634, 8654), self.input.position)
                _G_apply_1079, lastError = self._apply(self.rule_PatternElementChain, "PatternElementChain", [])
                self.considerError(lastError, None)
                return (_G_apply_1079, self.currentError)
            _G_many_1080, lastError = self.many(_G_many_1077)
            self.considerError(lastError, 'RelationshipsPattern')
            _locals['pec'] = _G_many_1080
            _G_python_1082, lastError = eval(self._G_expr_1081, self.globals, _locals), None
            self.considerError(lastError, 'RelationshipsPattern')
            return (_G_python_1082, self.currentError)


        def rule_GraphRelationshipsPattern(self):
            _locals = {'self': self}
            self.locals['GraphRelationshipsPattern'] = _locals
            self._trace(' ["Any", ', (8807, 8816), self.input.position)
            _G_apply_1083, lastError = self._apply(self.rule_Variable, "Variable", [])
            self.considerError(lastError, 'GraphRelationshipsPattern')
            _locals['v'] = _G_apply_1083
            self._trace('x]\n ', (8818, 8822), self.input.position)
            _G_exactly_1084, lastError = self.exactly(':')
            self.considerError(lastError, 'GraphRelationshipsPattern')
            self._trace('   ', (8822, 8825), self.input.position)
            _G_apply_1085, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'GraphRelationshipsPattern')
            self._trace('     | N O N', (8825, 8837), self.input.position)
            _G_apply_1086, lastError = self._apply(self.rule_NodePattern, "NodePattern", [])
            self.considerError(lastError, 'GraphRelationshipsPattern')
            _locals['np'] = _G_apply_1086
            def _G_many_1087():
                self._trace(" '", (8842, 8844), self.input.position)
                _G_apply_1088, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace("(' WS FilterExpressi", (8844, 8864), self.input.position)
                _G_apply_1089, lastError = self._apply(self.rule_PatternElementChain, "PatternElementChain", [])
                self.considerError(lastError, None)
                return (_G_apply_1089, self.currentError)
            _G_many_1090, lastError = self.many(_G_many_1087)
            self.considerError(lastError, 'GraphRelationshipsPattern')
            _locals['pec'] = _G_many_1090
            _G_python_1092, lastError = eval(self._G_expr_1091, self.globals, _locals), None
            self.considerError(lastError, 'GraphRelationshipsPattern')
            return (_G_python_1092, self.currentError)


        def rule_ExplicitExistsExpression(self):
            _locals = {'self': self}
            self.locals['ExplicitExistsExpression'] = _locals
            self._trace('Gr', (9018, 9020), self.input.position)
            _G_apply_1093, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'ExplicitExistsExpression')
            self._trace('ap', (9020, 9022), self.input.position)
            _G_apply_1094, lastError = self._apply(self.rule_X, "X", [])
            self.considerError(lastError, 'ExplicitExistsExpression')
            self._trace('hR', (9022, 9024), self.input.position)
            _G_apply_1095, lastError = self._apply(self.rule_I, "I", [])
            self.considerError(lastError, 'ExplicitExistsExpression')
            self._trace('el', (9024, 9026), self.input.position)
            _G_apply_1096, lastError = self._apply(self.rule_S, "S", [])
            self.considerError(lastError, 'ExplicitExistsExpression')
            self._trace('at', (9026, 9028), self.input.position)
            _G_apply_1097, lastError = self._apply(self.rule_T, "T", [])
            self.considerError(lastError, 'ExplicitExistsExpression')
            self._trace('io', (9028, 9030), self.input.position)
            _G_apply_1098, lastError = self._apply(self.rule_S, "S", [])
            self.considerError(lastError, 'ExplicitExistsExpression')
            self._trace('nsh', (9030, 9033), self.input.position)
            _G_apply_1099, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'ExplicitExistsExpression')
            self._trace('ipsP', (9033, 9037), self.input.position)
            _G_apply_1100, lastError = self._apply(self.rule_token, "token", ["{"])
            self.considerError(lastError, 'ExplicitExistsExpression')
            self._trace('att', (9037, 9040), self.input.position)
            _G_apply_1101, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'ExplicitExistsExpression')
            self._trace('ern\n    ', (9040, 9048), self.input.position)
            _G_apply_1102, lastError = self._apply(self.rule_Pattern, "Pattern", [])
            self.considerError(lastError, 'ExplicitExistsExpression')
            _locals['p'] = _G_apply_1102
            def _G_optional_1103():
                self._trace(' |', (9052, 9054), self.input.position)
                _G_apply_1104, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace(' Expli', (9054, 9060), self.input.position)
                _G_apply_1105, lastError = self._apply(self.rule_Where, "Where", [])
                self.considerError(lastError, None)
                return (_G_apply_1105, self.currentError)
            def _G_optional_1106():
                return (None, self.input.nullError())
            _G_or_1107, lastError = self._or([_G_optional_1103, _G_optional_1106])
            self.considerError(lastError, 'ExplicitExistsExpression')
            _locals['w'] = _G_or_1107
            self._trace('xis', (9064, 9067), self.input.position)
            _G_apply_1108, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'ExplicitExistsExpression')
            self._trace('tsEx', (9067, 9071), self.input.position)
            _G_apply_1109, lastError = self._apply(self.rule_token, "token", ["}"])
            self.considerError(lastError, 'ExplicitExistsExpression')
            _G_python_1111, lastError = eval(self._G_expr_1110, self.globals, _locals), None
            self.considerError(lastError, 'ExplicitExistsExpression')
            return (_G_python_1111, self.currentError)


        def rule_ExistsFunction(self):
            _locals = {'self': self}
            self.locals['ExistsFunction'] = _locals
            self._trace('ze', (9127, 9129), self.input.position)
            _G_apply_1112, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'ExistsFunction')
            self._trace('dE', (9129, 9131), self.input.position)
            _G_apply_1113, lastError = self._apply(self.rule_X, "X", [])
            self.considerError(lastError, 'ExistsFunction')
            self._trace('xp', (9131, 9133), self.input.position)
            _G_apply_1114, lastError = self._apply(self.rule_I, "I", [])
            self.considerError(lastError, 'ExistsFunction')
            self._trace('re', (9133, 9135), self.input.position)
            _G_apply_1115, lastError = self._apply(self.rule_S, "S", [])
            self.considerError(lastError, 'ExistsFunction')
            self._trace('ss', (9135, 9137), self.input.position)
            _G_apply_1116, lastError = self._apply(self.rule_T, "T", [])
            self.considerError(lastError, 'ExistsFunction')
            self._trace('io', (9137, 9139), self.input.position)
            _G_apply_1117, lastError = self._apply(self.rule_S, "S", [])
            self.considerError(lastError, 'ExistsFunction')
            self._trace('n\n ', (9139, 9142), self.input.position)
            _G_apply_1118, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'ExistsFunction')
            self._trace('    ', (9142, 9146), self.input.position)
            _G_apply_1119, lastError = self._apply(self.rule_token, "token", ["("])
            self.considerError(lastError, 'ExistsFunction')
            self._trace('   ', (9146, 9149), self.input.position)
            _G_apply_1120, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'ExistsFunction')
            self._trace(' | Funct', (9149, 9157), self.input.position)
            _G_apply_1121, lastError = self._apply(self.rule_Pattern, "Pattern", [])
            self.considerError(lastError, 'ExistsFunction')
            _locals['p'] = _G_apply_1121
            self._trace('nIn', (9159, 9162), self.input.position)
            _G_apply_1122, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'ExistsFunction')
            self._trace('voca', (9162, 9166), self.input.position)
            _G_apply_1123, lastError = self._apply(self.rule_token, "token", [")"])
            self.considerError(lastError, 'ExistsFunction')
            _G_python_1125, lastError = eval(self._G_expr_1124, self.globals, _locals), None
            self.considerError(lastError, 'ExistsFunction')
            return (_G_python_1125, self.currentError)


        def rule_FilterExpression(self):
            _locals = {'self': self}
            self.locals['FilterExpression'] = _locals
            self._trace("on = '(' ", (9217, 9226), self.input.position)
            _G_apply_1126, lastError = self._apply(self.rule_IdInColl, "IdInColl", [])
            self.considerError(lastError, 'FilterExpression')
            _locals['i'] = _G_apply_1126
            def _G_optional_1127():
                self._trace('xp', (9230, 9232), self.input.position)
                _G_apply_1128, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('ressio', (9232, 9238), self.input.position)
                _G_apply_1129, lastError = self._apply(self.rule_Where, "Where", [])
                self.considerError(lastError, None)
                return (_G_apply_1129, self.currentError)
            def _G_optional_1130():
                return (None, self.input.nullError())
            _G_or_1131, lastError = self._or([_G_optional_1127, _G_optional_1130])
            self.considerError(lastError, 'FilterExpression')
            _locals['w'] = _G_or_1131
            _G_python_1133, lastError = eval(self._G_expr_1132, self.globals, _locals), None
            self.considerError(lastError, 'FilterExpression')
            return (_G_python_1133, self.currentError)


        def rule_IdInColl(self):
            _locals = {'self': self}
            self.locals['IdInColl'] = _locals
            self._trace('NodePatte', (9284, 9293), self.input.position)
            _G_apply_1134, lastError = self._apply(self.rule_Variable, "Variable", [])
            self.considerError(lastError, 'IdInColl')
            _locals['v'] = _G_apply_1134
            self._trace(':np', (9295, 9298), self.input.position)
            _G_apply_1135, lastError = self._apply(self.rule_SP, "SP", [])
            self.considerError(lastError, 'IdInColl')
            self._trace(' (', (9298, 9300), self.input.position)
            _G_apply_1136, lastError = self._apply(self.rule_I, "I", [])
            self.considerError(lastError, 'IdInColl')
            self._trace('WS', (9300, 9302), self.input.position)
            _G_apply_1137, lastError = self._apply(self.rule_N, "N", [])
            self.considerError(lastError, 'IdInColl')
            self._trace(' Pa', (9302, 9305), self.input.position)
            _G_apply_1138, lastError = self._apply(self.rule_SP, "SP", [])
            self.considerError(lastError, 'IdInColl')
            self._trace('tternElemen', (9305, 9316), self.input.position)
            _G_apply_1139, lastError = self._apply(self.rule_Expression, "Expression", [])
            self.considerError(lastError, 'IdInColl')
            _locals['ex'] = _G_apply_1139
            _G_python_1141, lastError = eval(self._G_expr_1140, self.globals, _locals), None
            self.considerError(lastError, 'IdInColl')
            return (_G_python_1141, self.currentError)


        def rule_FunctionInvocation(self):
            _locals = {'self': self}
            self.locals['FunctionInvocation'] = _locals
            self._trace('ImplicitExist', (9364, 9377), self.input.position)
            _G_apply_1142, lastError = self._apply(self.rule_FunctionName, "FunctionName", [])
            self.considerError(lastError, 'FunctionInvocation')
            _locals['func'] = _G_apply_1142
            self._trace('ession", [[\'PatternPart', (9382, 9405), self.input.position)
            _G_apply_1143, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'FunctionInvocation')
            self._trace("', N", (9405, 9409), self.input.position)
            _G_exactly_1144, lastError = self.exactly('(')
            self.considerError(lastError, 'FunctionInvocation')
            self._trace('one', (9409, 9412), self.input.position)
            _G_apply_1145, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'FunctionInvocation')
            def _G_optional_1146():
                self._trace('p', (9434, 9435), self.input.position)
                _G_apply_1147, lastError = self._apply(self.rule_D, "D", [])
                self.considerError(lastError, None)
                self._trace(', ', (9435, 9437), self.input.position)
                _G_apply_1148, lastError = self._apply(self.rule_I, "I", [])
                self.considerError(lastError, None)
                self._trace('pe', (9437, 9439), self.input.position)
                _G_apply_1149, lastError = self._apply(self.rule_S, "S", [])
                self.considerError(lastError, None)
                self._trace('c]', (9439, 9441), self.input.position)
                _G_apply_1150, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                self._trace(']]', (9441, 9443), self.input.position)
                _G_apply_1151, lastError = self._apply(self.rule_I, "I", [])
                self.considerError(lastError, None)
                self._trace(', ', (9443, 9445), self.input.position)
                _G_apply_1152, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace('No', (9445, 9447), self.input.position)
                _G_apply_1153, lastError = self._apply(self.rule_C, "C", [])
                self.considerError(lastError, None)
                self._trace('ne', (9447, 9449), self.input.position)
                _G_apply_1154, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                self._trace(']\n ', (9449, 9452), self.input.position)
                _G_apply_1155, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                _G_python_1156, lastError = ("distinct"), None
                self.considerError(lastError, None)
                return (_G_python_1156, self.currentError)
            def _G_optional_1157():
                return (None, self.input.nullError())
            _G_or_1158, lastError = self._or([_G_optional_1146, _G_optional_1157])
            self.considerError(lastError, 'FunctionInvocation')
            _locals['distinct'] = _G_or_1158
            def _G_or_1159():
                self._trace("':' WS NodePattern:np (WS PatternEl", (9499, 9534), self.input.position)
                _G_apply_1160, lastError = self._apply(self.rule_Expression, "Expression", [])
                self.considerError(lastError, None)
                _locals['head'] = _G_apply_1160
                def _G_many_1161():
                    self._trace('                -> ["ImplicitExi', (9565, 9597), self.input.position)
                    _G_exactly_1162, lastError = self.exactly(',')
                    self.considerError(lastError, None)
                    self._trace('sts', (9597, 9600), self.input.position)
                    _G_apply_1163, lastError = self._apply(self.rule_WS, "WS", [])
                    self.considerError(lastError, None)
                    self._trace('Expression"', (9600, 9611), self.input.position)
                    _G_apply_1164, lastError = self._apply(self.rule_Expression, "Expression", [])
                    self.considerError(lastError, None)
                    return (_G_apply_1164, self.currentError)
                _G_many_1165, lastError = self.many(_G_many_1161)
                self.considerError(lastError, None)
                _locals['tail'] = _G_many_1165
                _G_python_1166, lastError = eval(self._G_expr_443, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_1166, self.currentError)
            def _G_or_1167():
                _G_python_1168, lastError = ([]), None
                self.considerError(lastError, None)
                return (_G_python_1168, self.currentError)
            _G_or_1169, lastError = self._or([_G_or_1159, _G_or_1167])
            self.considerError(lastError, 'FunctionInvocation')
            _locals['args'] = _G_or_1169
            self._trace('T S WS "{" WS Pattern:p', (9715, 9738), self.input.position)
            _G_apply_1170, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'FunctionInvocation')
            self._trace(' (WS', (9738, 9742), self.input.position)
            _G_exactly_1171, lastError = self.exactly(')')
            self.considerError(lastError, 'FunctionInvocation')
            _G_python_1173, lastError = eval(self._G_expr_1172, self.globals, _locals), None
            self.considerError(lastError, 'FunctionInvocation')
            return (_G_python_1173, self.currentError)


        def rule_FunctionName(self):
            _locals = {'self': self}
            self.locals['FunctionName'] = _locals
            self._trace('p, w]\n\n    Ex', (9792, 9805), self.input.position)
            _G_apply_1174, lastError = self._apply(self.rule_SymbolicName, "SymbolicName", [])
            self.considerError(lastError, 'FunctionName')
            return (_G_apply_1174, self.currentError)


        def rule_ListComprehension(self):
            _locals = {'self': self}
            self.locals['ListComprehension'] = _locals
            self._trace('S T ', (9826, 9830), self.input.position)
            _G_exactly_1175, lastError = self.exactly('[')
            self.considerError(lastError, 'ListComprehension')
            self._trace('S WS "(" WS Patte', (9830, 9847), self.input.position)
            _G_apply_1176, lastError = self._apply(self.rule_FilterExpression, "FilterExpression", [])
            self.considerError(lastError, 'ListComprehension')
            _locals['fex'] = _G_apply_1176
            def _G_optional_1177():
                self._trace('S ', (9853, 9855), self.input.position)
                _G_apply_1178, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('")" ', (9855, 9859), self.input.position)
                _G_exactly_1179, lastError = self.exactly('|')
                self.considerError(lastError, None)
                self._trace('-> ["Exists', (9859, 9870), self.input.position)
                _G_apply_1180, lastError = self._apply(self.rule_Expression, "Expression", [])
                self.considerError(lastError, None)
                return (_G_apply_1180, self.currentError)
            def _G_optional_1181():
                return (None, self.input.nullError())
            _G_or_1182, lastError = self._or([_G_optional_1177, _G_optional_1181])
            self.considerError(lastError, 'ListComprehension')
            _locals['ex'] = _G_or_1182
            self._trace('ion"', (9875, 9879), self.input.position)
            _G_exactly_1183, lastError = self.exactly(']')
            self.considerError(lastError, 'ListComprehension')
            _G_python_1185, lastError = eval(self._G_expr_1184, self.globals, _locals), None
            self.considerError(lastError, 'ListComprehension')
            return (_G_python_1185, self.currentError)


        def rule_PropertyLookup(self):
            _locals = {'self': self}
            self.locals['PropertyLookup'] = _locals
            self._trace('ess', (10010, 10013), self.input.position)
            _G_apply_1186, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'PropertyLookup')
            self._trace('ion:', (10013, 10017), self.input.position)
            _G_exactly_1187, lastError = self.exactly('.')
            self.considerError(lastError, 'PropertyLookup')
            self._trace('ex ', (10017, 10020), self.input.position)
            _G_apply_1188, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'PropertyLookup')
            self._trace('-> ["IdInColl", ', (10020, 10036), self.input.position)
            _G_apply_1189, lastError = self._apply(self.rule_PropertyKeyName, "PropertyKeyName", [])
            self.considerError(lastError, 'PropertyLookup')
            _locals['n'] = _G_apply_1189
            _G_python_1191, lastError = eval(self._G_expr_1190, self.globals, _locals), None
            self.considerError(lastError, 'PropertyLookup')
            return (_G_python_1191, self.currentError)


        def rule_CaseExpression(self):
            _locals = {'self': self}
            self.locals['CaseExpression'] = _locals
            self._trace(':func\n             ', (10081, 10100), self.input.position)
            _G_apply_1192, lastError = self._apply(self.rule_C, "C", [])
            self.considerError(lastError, 'CaseExpression')
            self._trace('  ', (10100, 10102), self.input.position)
            _G_apply_1193, lastError = self._apply(self.rule_A, "A", [])
            self.considerError(lastError, 'CaseExpression')
            self._trace('  ', (10102, 10104), self.input.position)
            _G_apply_1194, lastError = self._apply(self.rule_S, "S", [])
            self.considerError(lastError, 'CaseExpression')
            self._trace('  ', (10104, 10106), self.input.position)
            _G_apply_1195, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'CaseExpression')
            self._trace('   ', (10106, 10109), self.input.position)
            _G_apply_1196, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'CaseExpression')
            def _G_optional_1197():
                self._trace('          ', (10128, 10138), self.input.position)
                _G_apply_1198, lastError = self._apply(self.rule_Expression, "Expression", [])
                self.considerError(lastError, None)
                return (_G_apply_1198, self.currentError)
            def _G_optional_1199():
                return (None, self.input.nullError())
            _G_or_1200, lastError = self._or([_G_optional_1197, _G_optional_1199])
            self.considerError(lastError, 'CaseExpression')
            _locals['ex'] = _G_or_1200
            def _G_many1_1201():
                self._trace('WS', (10162, 10164), self.input.position)
                _G_apply_1202, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace(' -> "distinct")?:', (10164, 10181), self.input.position)
                _G_apply_1203, lastError = self._apply(self.rule_CaseAlternatives, "CaseAlternatives", [])
                self.considerError(lastError, None)
                return (_G_apply_1203, self.currentError)
            _G_many1_1204, lastError = self.many(_G_many1_1201, _G_many1_1201())
            self.considerError(lastError, 'CaseExpression')
            _locals['cas'] = _G_many1_1204
            def _G_optional_1205():
                self._trace('  ', (10207, 10209), self.input.position)
                _G_apply_1206, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('  ', (10209, 10211), self.input.position)
                _G_apply_1207, lastError = self._apply(self.rule_E, "E", [])
                self.considerError(lastError, None)
                self._trace('  ', (10211, 10213), self.input.position)
                _G_apply_1208, lastError = self._apply(self.rule_L, "L", [])
                self.considerError(lastError, None)
                self._trace(' (', (10213, 10215), self.input.position)
                _G_apply_1209, lastError = self._apply(self.rule_S, "S", [])
                self.considerError(lastError, None)
                self._trace('\n ', (10215, 10217), self.input.position)
                _G_apply_1210, lastError = self._apply(self.rule_E, "E", [])
                self.considerError(lastError, None)
                self._trace('   ', (10217, 10220), self.input.position)
                _G_apply_1211, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('           ', (10220, 10231), self.input.position)
                _G_apply_1212, lastError = self._apply(self.rule_Expression, "Expression", [])
                self.considerError(lastError, None)
                return (_G_apply_1212, self.currentError)
            def _G_optional_1213():
                return (None, self.input.nullError())
            _G_or_1214, lastError = self._or([_G_optional_1205, _G_optional_1213])
            self.considerError(lastError, 'CaseExpression')
            _locals['el'] = _G_or_1214
            self._trace('        Expression:h', (10236, 10256), self.input.position)
            _G_apply_1215, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'CaseExpression')
            self._trace('ea', (10256, 10258), self.input.position)
            _G_apply_1216, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'CaseExpression')
            self._trace('d\n', (10258, 10260), self.input.position)
            _G_apply_1217, lastError = self._apply(self.rule_N, "N", [])
            self.considerError(lastError, 'CaseExpression')
            self._trace('  ', (10260, 10262), self.input.position)
            _G_apply_1218, lastError = self._apply(self.rule_D, "D", [])
            self.considerError(lastError, 'CaseExpression')
            _G_python_1220, lastError = eval(self._G_expr_1219, self.globals, _locals), None
            self.considerError(lastError, 'CaseExpression')
            return (_G_python_1220, self.currentError)


        def rule_CaseAlternatives(self):
            _locals = {'self': self}
            self.locals['CaseAlternatives'] = _locals
            self._trace("' ", (10324, 10326), self.input.position)
            _G_apply_1221, lastError = self._apply(self.rule_W, "W", [])
            self.considerError(lastError, 'CaseAlternatives')
            self._trace('WS', (10326, 10328), self.input.position)
            _G_apply_1222, lastError = self._apply(self.rule_H, "H", [])
            self.considerError(lastError, 'CaseAlternatives')
            self._trace(' E', (10328, 10330), self.input.position)
            _G_apply_1223, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'CaseAlternatives')
            self._trace('xp', (10330, 10332), self.input.position)
            _G_apply_1224, lastError = self._apply(self.rule_N, "N", [])
            self.considerError(lastError, 'CaseAlternatives')
            self._trace('res', (10332, 10335), self.input.position)
            _G_apply_1225, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'CaseAlternatives')
            self._trace('sion\n      ', (10335, 10346), self.input.position)
            _G_apply_1226, lastError = self._apply(self.rule_Expression, "Expression", [])
            self.considerError(lastError, 'CaseAlternatives')
            _locals['ex1'] = _G_apply_1226
            self._trace('   ', (10350, 10353), self.input.position)
            _G_apply_1227, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'CaseAlternatives')
            self._trace('  ', (10353, 10355), self.input.position)
            _G_apply_1228, lastError = self._apply(self.rule_T, "T", [])
            self.considerError(lastError, 'CaseAlternatives')
            self._trace('  ', (10355, 10357), self.input.position)
            _G_apply_1229, lastError = self._apply(self.rule_H, "H", [])
            self.considerError(lastError, 'CaseAlternatives')
            self._trace('  ', (10357, 10359), self.input.position)
            _G_apply_1230, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'CaseAlternatives')
            self._trace('  ', (10359, 10361), self.input.position)
            _G_apply_1231, lastError = self._apply(self.rule_N, "N", [])
            self.considerError(lastError, 'CaseAlternatives')
            self._trace('   ', (10361, 10364), self.input.position)
            _G_apply_1232, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'CaseAlternatives')
            self._trace('    )*:tail', (10364, 10375), self.input.position)
            _G_apply_1233, lastError = self._apply(self.rule_Expression, "Expression", [])
            self.considerError(lastError, 'CaseAlternatives')
            _locals['ex2'] = _G_apply_1233
            _G_python_1235, lastError = eval(self._G_expr_1234, self.globals, _locals), None
            self.considerError(lastError, 'CaseAlternatives')
            return (_G_python_1235, self.currentError)


        def rule_Variable(self):
            _locals = {'self': self}
            self.locals['Variable'] = _locals
            self._trace('            |', (10405, 10418), self.input.position)
            _G_apply_1236, lastError = self._apply(self.rule_SymbolicName, "SymbolicName", [])
            self.considerError(lastError, 'Variable')
            _locals['s'] = _G_apply_1236
            _G_python_1238, lastError = eval(self._G_expr_1237, self.globals, _locals), None
            self.considerError(lastError, 'Variable')
            return (_G_python_1238, self.currentError)


        def rule_StringLiteral(self):
            _locals = {'self': self}
            self.locals['StringLiteral'] = _locals
            def _G_or_1239():
                self._trace('                  ', (10458, 10476), self.input.position)
                _G_exactly_1240, lastError = self.exactly('"')
                self.considerError(lastError, None)
                def _G_many_1241():
                    def _G_or_1242():
                        def _G_not_1243():
                            def _G_or_1244():
                                self._trace('WS ', (10480, 10483), self.input.position)
                                _G_exactly_1245, lastError = self.exactly('"')
                                self.considerError(lastError, None)
                                return (_G_exactly_1245, self.currentError)
                            def _G_or_1246():
                                self._trace(")' -", (10484, 10488), self.input.position)
                                _G_exactly_1247, lastError = self.exactly('\\')
                                self.considerError(lastError, None)
                                return (_G_exactly_1247, self.currentError)
                            _G_or_1248, lastError = self._or([_G_or_1244, _G_or_1246])
                            self.considerError(lastError, None)
                            return (_G_or_1248, self.currentError)
                        _G_not_1249, lastError = self._not(_G_not_1243)
                        self.considerError(lastError, None)
                        self._trace(' ["call",', (10489, 10498), self.input.position)
                        _G_apply_1250, lastError = self._apply(self.rule_anything, "anything", [])
                        self.considerError(lastError, None)
                        return (_G_apply_1250, self.currentError)
                    def _G_or_1251():
                        self._trace('unc, distinc', (10500, 10512), self.input.position)
                        _G_apply_1252, lastError = self._apply(self.rule_EscapedChar, "EscapedChar", [])
                        self.considerError(lastError, None)
                        return (_G_apply_1252, self.currentError)
                    _G_or_1253, lastError = self._or([_G_or_1242, _G_or_1251])
                    self.considerError(lastError, None)
                    return (_G_or_1253, self.currentError)
                _G_many_1254, lastError = self.many(_G_many_1241)
                self.considerError(lastError, None)
                _locals['cs'] = _G_many_1254
                self._trace('gs]\n', (10517, 10521), self.input.position)
                _G_exactly_1255, lastError = self.exactly('"')
                self.considerError(lastError, None)
                _G_python_1257, lastError = eval(self._G_expr_1256, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_1257, self.currentError)
            def _G_or_1258():
                self._trace('e\n\n ', (10552, 10556), self.input.position)
                _G_apply_1259, lastError = self._apply(self.rule_token, "token", ["'"])
                self.considerError(lastError, None)
                def _G_many_1260():
                    def _G_or_1261():
                        def _G_not_1262():
                            def _G_or_1263():
                                self._trace('ist', (10560, 10563), self.input.position)
                                _G_apply_1264, lastError = self._apply(self.rule_token, "token", ["'"])
                                self.considerError(lastError, None)
                                return (_G_apply_1264, self.currentError)
                            def _G_or_1265():
                                self._trace('ompr', (10564, 10568), self.input.position)
                                _G_exactly_1266, lastError = self.exactly('\\')
                                self.considerError(lastError, None)
                                return (_G_exactly_1266, self.currentError)
                            _G_or_1267, lastError = self._or([_G_or_1263, _G_or_1265])
                            self.considerError(lastError, None)
                            return (_G_or_1267, self.currentError)
                        _G_not_1268, lastError = self._not(_G_not_1262)
                        self.considerError(lastError, None)
                        self._trace('hension =', (10569, 10578), self.input.position)
                        _G_apply_1269, lastError = self._apply(self.rule_anything, "anything", [])
                        self.considerError(lastError, None)
                        return (_G_apply_1269, self.currentError)
                    def _G_or_1270():
                        self._trace("[' FilterExp", (10580, 10592), self.input.position)
                        _G_apply_1271, lastError = self._apply(self.rule_EscapedChar, "EscapedChar", [])
                        self.considerError(lastError, None)
                        return (_G_apply_1271, self.currentError)
                    _G_or_1272, lastError = self._or([_G_or_1261, _G_or_1270])
                    self.considerError(lastError, None)
                    return (_G_or_1272, self.currentError)
                _G_many_1273, lastError = self.many(_G_many_1260)
                self.considerError(lastError, None)
                _locals['cs'] = _G_many_1273
                self._trace('on:f', (10597, 10601), self.input.position)
                _G_apply_1274, lastError = self._apply(self.rule_token, "token", ["'"])
                self.considerError(lastError, None)
                _G_python_1275, lastError = eval(self._G_expr_1256, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_1275, self.currentError)
            _G_or_1276, lastError = self._or([_G_or_1239, _G_or_1258])
            self.considerError(lastError, 'StringLiteral')
            _locals['l'] = _G_or_1276
            _G_python_1278, lastError = eval(self._G_expr_1277, self.globals, _locals), None
            self.considerError(lastError, 'StringLiteral')
            return (_G_python_1278, self.currentError)


        def rule_EscapedChar(self):
            _locals = {'self': self}
            self.locals['EscapedChar'] = _locals
            self._trace('    #', (10667, 10672), self.input.position)
            _G_exactly_1279, lastError = self.exactly('\\')
            self.considerError(lastError, 'EscapedChar')
            def _G_or_1280():
                self._trace('p = ', (10686, 10690), self.input.position)
                _G_exactly_1281, lastError = self.exactly('\\')
                self.considerError(lastError, None)
                _G_python_1282, lastError = ('\\'), None
                self.considerError(lastError, None)
                return (_G_python_1282, self.currentError)
            def _G_or_1283():
                self._trace('yNam', (10712, 10716), self.input.position)
                _G_apply_1284, lastError = self._apply(self.rule_token, "token", ["'"])
                self.considerError(lastError, None)
                _G_python_1285, lastError = ("'"), None
                self.considerError(lastError, None)
                return (_G_python_1285, self.currentError)
            def _G_or_1286():
                self._trace('erty', (10737, 10741), self.input.position)
                _G_exactly_1287, lastError = self.exactly('"')
                self.considerError(lastError, None)
                _G_python_1288, lastError = ('"'), None
                self.considerError(lastError, None)
                return (_G_python_1288, self.currentError)
            def _G_or_1289():
                self._trace('Lo', (10762, 10764), self.input.position)
                _G_apply_1290, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                _G_python_1291, lastError = ('\n'), None
                self.considerError(lastError, None)
                return (_G_python_1291, self.currentError)
            def _G_or_1292():
                self._trace('rt', (10786, 10788), self.input.position)
                _G_apply_1293, lastError = self._apply(self.rule_R, "R", [])
                self.considerError(lastError, None)
                _G_python_1294, lastError = ('\r'), None
                self.considerError(lastError, None)
                return (_G_python_1294, self.currentError)
            def _G_or_1295():
                self._trace('ty', (10810, 10812), self.input.position)
                _G_apply_1296, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                _G_python_1297, lastError = ('\t'), None
                self.considerError(lastError, None)
                return (_G_python_1297, self.currentError)
            def _G_or_1298():
                self._trace('xpre', (10834, 10838), self.input.position)
                _G_exactly_1299, lastError = self.exactly('_')
                self.considerError(lastError, None)
                _G_python_1300, lastError = ('_'), None
                self.considerError(lastError, None)
                return (_G_python_1300, self.currentError)
            def _G_or_1301():
                self._trace('    ', (10859, 10863), self.input.position)
                _G_exactly_1302, lastError = self.exactly('%')
                self.considerError(lastError, None)
                _G_python_1303, lastError = ('%'), None
                self.considerError(lastError, None)
                return (_G_python_1303, self.currentError)
            _G_or_1304, lastError = self._or([_G_or_1280, _G_or_1283, _G_or_1286, _G_or_1289, _G_or_1292, _G_or_1295, _G_or_1298, _G_or_1301])
            self.considerError(lastError, 'EscapedChar')
            return (_G_or_1304, self.currentError)


        def rule_NumberLiteral(self):
            _locals = {'self': self}
            self.locals['NumberLiteral'] = _locals
            def _G_or_1305():
                self._trace('ression)?:ex\n               ', (10903, 10931), self.input.position)
                _G_apply_1306, lastError = self._apply(self.rule_DoubleLiteral, "DoubleLiteral", [])
                self.considerError(lastError, None)
                return (_G_apply_1306, self.currentError)
            def _G_or_1307():
                self._trace('ternatives)+:ca', (10947, 10962), self.input.position)
                _G_apply_1308, lastError = self._apply(self.rule_IntegerLiteral, "IntegerLiteral", [])
                self.considerError(lastError, None)
                return (_G_apply_1308, self.currentError)
            _G_or_1309, lastError = self._or([_G_or_1305, _G_or_1307])
            self.considerError(lastError, 'NumberLiteral')
            _locals['l'] = _G_or_1309
            _G_python_1310, lastError = eval(self._G_expr_1277, self.globals, _locals), None
            self.considerError(lastError, 'NumberLiteral')
            return (_G_python_1310, self.currentError)


        def rule_MapLiteral(self):
            _locals = {'self': self}
            self.locals['MapLiteral'] = _locals
            self._trace('?:el', (11012, 11016), self.input.position)
            _G_exactly_1311, lastError = self.exactly('{')
            self.considerError(lastError, 'MapLiteral')
            self._trace('\n  ', (11016, 11019), self.input.position)
            _G_apply_1312, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'MapLiteral')
            def _G_or_1313():
                self._trace('                -> ["Case", ex, cas,', (11052, 11088), self.input.position)
                _G_apply_1314, lastError = self._apply(self.rule_PropertyKeyName, "PropertyKeyName", [])
                self.considerError(lastError, None)
                _locals['k'] = _G_apply_1314
                self._trace('l]\n', (11090, 11093), self.input.position)
                _G_apply_1315, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('\n   ', (11093, 11097), self.input.position)
                _G_exactly_1316, lastError = self.exactly(':')
                self.considerError(lastError, None)
                self._trace(' Ca', (11097, 11100), self.input.position)
                _G_apply_1317, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('seAlternati', (11100, 11111), self.input.position)
                _G_apply_1318, lastError = self._apply(self.rule_Expression, "Expression", [])
                self.considerError(lastError, None)
                _locals['v'] = _G_apply_1318
                _G_python_1320, lastError = eval(self._G_expr_1319, self.globals, _locals), None
                self.considerError(lastError, None)
                _locals['head'] = _G_python_1320
                self._trace('T H', (11146, 11149), self.input.position)
                _G_apply_1321, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                def _G_many_1322():
                    self._trace(':ex2 -> [ex1, ex2]\n\n    ', (11167, 11191), self.input.position)
                    _G_exactly_1323, lastError = self.exactly(',')
                    self.considerError(lastError, None)
                    self._trace('Var', (11191, 11194), self.input.position)
                    _G_apply_1324, lastError = self._apply(self.rule_WS, "WS", [])
                    self.considerError(lastError, None)
                    self._trace('iable = Symbolic', (11194, 11210), self.input.position)
                    _G_apply_1325, lastError = self._apply(self.rule_PropertyKeyName, "PropertyKeyName", [])
                    self.considerError(lastError, None)
                    _locals['k'] = _G_apply_1325
                    self._trace('me:', (11212, 11215), self.input.position)
                    _G_apply_1326, lastError = self._apply(self.rule_WS, "WS", [])
                    self.considerError(lastError, None)
                    self._trace('s ->', (11215, 11219), self.input.position)
                    _G_exactly_1327, lastError = self.exactly(':')
                    self.considerError(lastError, None)
                    self._trace(' ["', (11219, 11222), self.input.position)
                    _G_apply_1328, lastError = self._apply(self.rule_WS, "WS", [])
                    self.considerError(lastError, None)
                    self._trace('Variable", ', (11222, 11233), self.input.position)
                    _G_apply_1329, lastError = self._apply(self.rule_Expression, "Expression", [])
                    self.considerError(lastError, None)
                    _locals['v'] = _G_apply_1329
                    self._trace('\n\n ', (11235, 11238), self.input.position)
                    _G_apply_1330, lastError = self._apply(self.rule_WS, "WS", [])
                    self.considerError(lastError, None)
                    _G_python_1331, lastError = eval(self._G_expr_1319, self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_1331, self.currentError)
                _G_many_1332, lastError = self.many(_G_many_1322)
                self.considerError(lastError, None)
                _locals['tail'] = _G_many_1332
                _G_python_1333, lastError = eval(self._G_expr_443, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_1333, self.currentError)
            def _G_or_1334():
                _G_python_1335, lastError = ([]), None
                self.considerError(lastError, None)
                return (_G_python_1335, self.currentError)
            _G_or_1336, lastError = self._or([_G_or_1313, _G_or_1334])
            self.considerError(lastError, 'MapLiteral')
            _locals['pairs'] = _G_or_1336
            self._trace('*:cs \'"\' -> "".j', (11317, 11333), self.input.position)
            _G_exactly_1337, lastError = self.exactly('}')
            self.considerError(lastError, 'MapLiteral')
            _G_python_1339, lastError = eval(self._G_expr_1338, self.globals, _locals), None
            self.considerError(lastError, 'MapLiteral')
            return (_G_python_1339, self.currentError)


        def rule_Parameter(self):
            _locals = {'self': self}
            self.locals['Parameter'] = _locals
            self._trace("\\') ", (11374, 11378), self.input.position)
            _G_exactly_1340, lastError = self.exactly('$')
            self.considerError(lastError, 'Parameter')
            def _G_or_1341():
                self._trace('ything | Esc', (11380, 11392), self.input.position)
                _G_apply_1342, lastError = self._apply(self.rule_SymbolicName, "SymbolicName", [])
                self.considerError(lastError, None)
                return (_G_apply_1342, self.currentError)
            def _G_or_1343():
                self._trace('edChar)*:cs "\'"', (11394, 11409), self.input.position)
                _G_apply_1344, lastError = self._apply(self.rule_DecimalInteger, "DecimalInteger", [])
                self.considerError(lastError, None)
                return (_G_apply_1344, self.currentError)
            _G_or_1345, lastError = self._or([_G_or_1341, _G_or_1343])
            self.considerError(lastError, 'Parameter')
            _locals['p'] = _G_or_1345
            _G_python_1347, lastError = eval(self._G_expr_1346, self.globals, _locals), None
            self.considerError(lastError, 'Parameter')
            return (_G_python_1347, self.currentError)


        def rule_PropertyExpression(self):
            _locals = {'self': self}
            self.locals['PropertyExpression'] = _locals
            self._trace('teral', (11454, 11459), self.input.position)
            _G_apply_1348, lastError = self._apply(self.rule_Atom, "Atom", [])
            self.considerError(lastError, 'PropertyExpression')
            _locals['a'] = _G_apply_1348
            def _G_many_1349():
                self._trace(']\n', (11463, 11465), self.input.position)
                _G_apply_1350, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('\n    EscapedCha', (11465, 11480), self.input.position)
                _G_apply_1351, lastError = self._apply(self.rule_PropertyLookup, "PropertyLookup", [])
                self.considerError(lastError, None)
                return (_G_apply_1351, self.currentError)
            _G_many_1352, lastError = self.many(_G_many_1349)
            self.considerError(lastError, 'PropertyExpression')
            _locals['opts'] = _G_many_1352
            _G_python_1354, lastError = eval(self._G_expr_1353, self.globals, _locals), None
            self.considerError(lastError, 'PropertyExpression')
            return (_G_python_1354, self.currentError)


        def rule_PropertyKeyName(self):
            _locals = {'self': self}
            self.locals['PropertyKeyName'] = _locals
            self._trace('  | "\'" -> "\'', (11533, 11546), self.input.position)
            _G_apply_1355, lastError = self._apply(self.rule_SymbolicName, "SymbolicName", [])
            self.considerError(lastError, 'PropertyKeyName')
            return (_G_apply_1355, self.currentError)


        def rule_IntegerLiteral(self):
            _locals = {'self': self}
            self.locals['IntegerLiteral'] = _locals
            def _G_or_1356():
                self._trace('| \'"\' -> \'"', (11564, 11575), self.input.position)
                _G_apply_1357, lastError = self._apply(self.rule_HexInteger, "HexInteger", [])
                self.considerError(lastError, None)
                return (_G_apply_1357, self.currentError)
            def _G_or_1358():
                self._trace(" | N -> '\\n'\n", (11592, 11605), self.input.position)
                _G_apply_1359, lastError = self._apply(self.rule_OctalInteger, "OctalInteger", [])
                self.considerError(lastError, None)
                return (_G_apply_1359, self.currentError)
            def _G_or_1360():
                self._trace(" R -> '\\r'\n    ", (11622, 11637), self.input.position)
                _G_apply_1361, lastError = self._apply(self.rule_DecimalInteger, "DecimalInteger", [])
                self.considerError(lastError, None)
                return (_G_apply_1361, self.currentError)
            _G_or_1362, lastError = self._or([_G_or_1356, _G_or_1358, _G_or_1360])
            self.considerError(lastError, 'IntegerLiteral')
            return (_G_or_1362, self.currentError)


        def rule_OctalDigit(self):
            _locals = {'self': self}
            self.locals['OctalDigit'] = _locals
            def _G_not_1363():
                def _G_or_1364():
                    self._trace("> '", (11654, 11657), self.input.position)
                    _G_exactly_1365, lastError = self.exactly('8')
                    self.considerError(lastError, None)
                    return (_G_exactly_1365, self.currentError)
                def _G_or_1366():
                    self._trace("t'\n", (11658, 11661), self.input.position)
                    _G_exactly_1367, lastError = self.exactly('9')
                    self.considerError(lastError, None)
                    return (_G_exactly_1367, self.currentError)
                _G_or_1368, lastError = self._or([_G_or_1364, _G_or_1366])
                self.considerError(lastError, None)
                return (_G_or_1368, self.currentError)
            _G_not_1369, lastError = self._not(_G_not_1363)
            self.considerError(lastError, 'OctalDigit')
            self._trace('      ', (11662, 11668), self.input.position)
            _G_apply_1370, lastError = self._apply(self.rule_digit, "digit", [])
            self.considerError(lastError, 'OctalDigit')
            return (_G_apply_1370, self.currentError)


        def rule_OctalInteger(self):
            _locals = {'self': self}
            self.locals['OctalInteger'] = _locals
            self._trace("> '_", (11684, 11688), self.input.position)
            _G_exactly_1371, lastError = self.exactly('0')
            self.considerError(lastError, 'OctalInteger')
            def _G_consumedby_1372():
                def _G_many1_1373():
                    self._trace('          ', (11690, 11700), self.input.position)
                    _G_apply_1374, lastError = self._apply(self.rule_OctalDigit, "OctalDigit", [])
                    self.considerError(lastError, None)
                    return (_G_apply_1374, self.currentError)
                _G_many1_1375, lastError = self.many(_G_many1_1373, _G_many1_1373())
                self.considerError(lastError, None)
                return (_G_many1_1375, self.currentError)
            _G_consumedby_1376, lastError = self.consumedby(_G_consumedby_1372)
            self.considerError(lastError, 'OctalInteger')
            _locals['ds'] = _G_consumedby_1376
            _G_python_1378, lastError = eval(self._G_expr_1377, self.globals, _locals), None
            self.considerError(lastError, 'OctalInteger')
            return (_G_python_1378, self.currentError)


        def rule_HexDigit(self):
            _locals = {'self': self}
            self.locals['HexDigit'] = _locals
            def _G_or_1379():
                self._trace('    )\n', (11731, 11737), self.input.position)
                _G_apply_1380, lastError = self._apply(self.rule_digit, "digit", [])
                self.considerError(lastError, None)
                return (_G_apply_1380, self.currentError)
            def _G_or_1381():
                self._trace('  ', (11739, 11741), self.input.position)
                _G_apply_1382, lastError = self._apply(self.rule_A, "A", [])
                self.considerError(lastError, None)
                return (_G_apply_1382, self.currentError)
            def _G_or_1383():
                self._trace('um', (11743, 11745), self.input.position)
                _G_apply_1384, lastError = self._apply(self.rule_B, "B", [])
                self.considerError(lastError, None)
                return (_G_apply_1384, self.currentError)
            def _G_or_1385():
                self._trace('rL', (11747, 11749), self.input.position)
                _G_apply_1386, lastError = self._apply(self.rule_C, "C", [])
                self.considerError(lastError, None)
                return (_G_apply_1386, self.currentError)
            def _G_or_1387():
                self._trace('er', (11751, 11753), self.input.position)
                _G_apply_1388, lastError = self._apply(self.rule_D, "D", [])
                self.considerError(lastError, None)
                return (_G_apply_1388, self.currentError)
            def _G_or_1389():
                self._trace(' =', (11755, 11757), self.input.position)
                _G_apply_1390, lastError = self._apply(self.rule_E, "E", [])
                self.considerError(lastError, None)
                return (_G_apply_1390, self.currentError)
            def _G_or_1391():
                self._trace('\n ', (11759, 11761), self.input.position)
                _G_apply_1392, lastError = self._apply(self.rule_F, "F", [])
                self.considerError(lastError, None)
                return (_G_apply_1392, self.currentError)
            _G_or_1393, lastError = self._or([_G_or_1379, _G_or_1381, _G_or_1383, _G_or_1385, _G_or_1387, _G_or_1389, _G_or_1391])
            self.considerError(lastError, 'HexDigit')
            return (_G_or_1393, self.currentError)


        def rule_HexInteger(self):
            _locals = {'self': self}
            self.locals['HexInteger'] = _locals
            self._trace('   D', (11775, 11779), self.input.position)
            _G_exactly_1394, lastError = self.exactly('0')
            self.considerError(lastError, 'HexInteger')
            self._trace('ou', (11779, 11781), self.input.position)
            _G_apply_1395, lastError = self._apply(self.rule_X, "X", [])
            self.considerError(lastError, 'HexInteger')
            def _G_consumedby_1396():
                def _G_many1_1397():
                    self._trace('eLiteral', (11783, 11791), self.input.position)
                    _G_apply_1398, lastError = self._apply(self.rule_HexDigit, "HexDigit", [])
                    self.considerError(lastError, None)
                    return (_G_apply_1398, self.currentError)
                _G_many1_1399, lastError = self.many(_G_many1_1397, _G_many1_1397())
                self.considerError(lastError, None)
                return (_G_many1_1399, self.currentError)
            _G_consumedby_1400, lastError = self.consumedby(_G_consumedby_1396)
            self.considerError(lastError, 'HexInteger')
            _locals['ds'] = _G_consumedby_1400
            _G_python_1402, lastError = eval(self._G_expr_1401, self.globals, _locals), None
            self.considerError(lastError, 'HexInteger')
            return (_G_python_1402, self.currentError)


        def rule_DecimalInteger(self):
            _locals = {'self': self}
            self.locals['DecimalInteger'] = _locals
            def _G_consumedby_1403():
                def _G_many1_1404():
                    self._trace('     ', (11831, 11836), self.input.position)
                    _G_apply_1405, lastError = self._apply(self.rule_digit, "digit", [])
                    self.considerError(lastError, None)
                    return (_G_apply_1405, self.currentError)
                _G_many1_1406, lastError = self.many(_G_many1_1404, _G_many1_1404())
                self.considerError(lastError, None)
                return (_G_many1_1406, self.currentError)
            _G_consumedby_1407, lastError = self.consumedby(_G_consumedby_1403)
            self.considerError(lastError, 'DecimalInteger')
            _locals['ds'] = _G_consumedby_1407
            _G_python_1409, lastError = eval(self._G_expr_1408, self.globals, _locals), None
            self.considerError(lastError, 'DecimalInteger')
            return (_G_python_1409, self.currentError)


        def rule_DoubleLiteral(self):
            _locals = {'self': self}
            self.locals['DoubleLiteral'] = _locals
            def _G_or_1410():
                self._trace("   MapLiteral = '{' ", (11869, 11889), self.input.position)
                _G_apply_1411, lastError = self._apply(self.rule_ExponentDecimalReal, "ExponentDecimalReal", [])
                self.considerError(lastError, None)
                return (_G_apply_1411, self.currentError)
            def _G_or_1412():
                self._trace('    (\n             ', (11905, 11924), self.input.position)
                _G_apply_1413, lastError = self._apply(self.rule_RegularDecimalReal, "RegularDecimalReal", [])
                self.considerError(lastError, None)
                return (_G_apply_1413, self.currentError)
            _G_or_1414, lastError = self._or([_G_or_1410, _G_or_1412])
            self.considerError(lastError, 'DoubleLiteral')
            return (_G_or_1414, self.currentError)


        def rule_ExponentDecimalReal(self):
            _locals = {'self': self}
            self.locals['ExponentDecimalReal'] = _locals
            def _G_consumedby_1415():
                def _G_or_1416():
                    self._trace('       PropertyKey', (11950, 11968), self.input.position)
                    _G_apply_1417, lastError = self._apply(self.rule_RegularDecimalReal, "RegularDecimalReal", [])
                    self.considerError(lastError, None)
                    return (_G_apply_1417, self.currentError)
                def _G_or_1418():
                    self._trace("me:k WS ':' WS ", (11970, 11985), self.input.position)
                    _G_apply_1419, lastError = self._apply(self.rule_DecimalInteger, "DecimalInteger", [])
                    self.considerError(lastError, None)
                    return (_G_apply_1419, self.currentError)
                _G_or_1420, lastError = self._or([_G_or_1416, _G_or_1418])
                self.considerError(lastError, None)
                self._trace('xp', (11986, 11988), self.input.position)
                _G_apply_1421, lastError = self._apply(self.rule_E, "E", [])
                self.considerError(lastError, None)
                def _G_optional_1422():
                    def _G_or_1423():
                        self._trace('ssi', (11990, 11993), self.input.position)
                        _G_exactly_1424, lastError = self.exactly('+')
                        self.considerError(lastError, None)
                        return (_G_exactly_1424, self.currentError)
                    def _G_or_1425():
                        self._trace(':v -', (11995, 11999), self.input.position)
                        _G_exactly_1426, lastError = self.exactly('-')
                        self.considerError(lastError, None)
                        return (_G_exactly_1426, self.currentError)
                    _G_or_1427, lastError = self._or([_G_or_1423, _G_or_1425])
                    self.considerError(lastError, None)
                    return (_G_or_1427, self.currentError)
                def _G_optional_1428():
                    return (None, self.input.nullError())
                _G_or_1429, lastError = self._or([_G_optional_1422, _G_optional_1428])
                self.considerError(lastError, None)
                self._trace('(k, v)\n        ', (12001, 12016), self.input.position)
                _G_apply_1430, lastError = self._apply(self.rule_DecimalInteger, "DecimalInteger", [])
                self.considerError(lastError, None)
                return (_G_apply_1430, self.currentError)
            _G_consumedby_1431, lastError = self.consumedby(_G_consumedby_1415)
            self.considerError(lastError, 'ExponentDecimalReal')
            _locals['ds'] = _G_consumedby_1431
            _G_python_1433, lastError = eval(self._G_expr_1432, self.globals, _locals), None
            self.considerError(lastError, 'ExponentDecimalReal')
            return (_G_python_1433, self.currentError)


        def rule_RegularDecimalReal(self):
            _locals = {'self': self}
            self.locals['RegularDecimalReal'] = _locals
            def _G_or_1434():
                def _G_consumedby_1435():
                    def _G_many1_1436():
                        self._trace('(\n   ', (12058, 12063), self.input.position)
                        _G_apply_1437, lastError = self._apply(self.rule_digit, "digit", [])
                        self.considerError(lastError, None)
                        return (_G_apply_1437, self.currentError)
                    _G_many1_1438, lastError = self.many(_G_many1_1436, _G_many1_1436())
                    self.considerError(lastError, None)
                    self._trace('    ', (12064, 12068), self.input.position)
                    _G_exactly_1439, lastError = self.exactly('.')
                    self.considerError(lastError, None)
                    def _G_many1_1440():
                        self._trace('      ', (12068, 12074), self.input.position)
                        _G_apply_1441, lastError = self._apply(self.rule_digit, "digit", [])
                        self.considerError(lastError, None)
                        return (_G_apply_1441, self.currentError)
                    _G_many1_1442, lastError = self.many(_G_many1_1440, _G_many1_1440())
                    self.considerError(lastError, None)
                    return (_G_many1_1442, self.currentError)
                _G_consumedby_1443, lastError = self.consumedby(_G_consumedby_1435)
                self.considerError(lastError, None)
                return (_G_consumedby_1443, self.currentError)
            def _G_or_1444():
                def _G_consumedby_1445():
                    def _G_many1_1446():
                        self._trace("    '", (12080, 12085), self.input.position)
                        _G_apply_1447, lastError = self._apply(self.rule_digit, "digit", [])
                        self.considerError(lastError, None)
                        return (_G_apply_1447, self.currentError)
                    _G_many1_1448, lastError = self.many(_G_many1_1446, _G_many1_1446())
                    self.considerError(lastError, None)
                    self._trace("' WS", (12086, 12090), self.input.position)
                    _G_exactly_1449, lastError = self.exactly('.')
                    self.considerError(lastError, None)
                    return (_G_exactly_1449, self.currentError)
                _G_consumedby_1450, lastError = self.consumedby(_G_consumedby_1445)
                self.considerError(lastError, None)
                return (_G_consumedby_1450, self.currentError)
            def _G_or_1451():
                def _G_consumedby_1452():
                    self._trace('ert', (12095, 12098), self.input.position)
                    _G_exactly_1453, lastError = self.exactly('.')
                    self.considerError(lastError, None)
                    def _G_many1_1454():
                        self._trace('yKeyNa', (12098, 12104), self.input.position)
                        _G_apply_1455, lastError = self._apply(self.rule_digit, "digit", [])
                        self.considerError(lastError, None)
                        return (_G_apply_1455, self.currentError)
                    _G_many1_1456, lastError = self.many(_G_many1_1454, _G_many1_1454())
                    self.considerError(lastError, None)
                    return (_G_many1_1456, self.currentError)
                _G_consumedby_1457, lastError = self.consumedby(_G_consumedby_1452)
                self.considerError(lastError, None)
                return (_G_consumedby_1457, self.currentError)
            _G_or_1458, lastError = self._or([_G_or_1434, _G_or_1444, _G_or_1451])
            self.considerError(lastError, 'RegularDecimalReal')
            _locals['ds'] = _G_or_1458
            _G_python_1459, lastError = eval(self._G_expr_1432, self.globals, _locals), None
            self.considerError(lastError, 'RegularDecimalReal')
            return (_G_python_1459, self.currentError)


        def rule_SymbolicName(self):
            _locals = {'self': self}
            self.locals['SymbolicName'] = _locals
            def _G_or_1460():
                self._trace('k, v)\n                ', (12139, 12161), self.input.position)
                _G_apply_1461, lastError = self._apply(self.rule_UnescapedSymbolicName, "UnescapedSymbolicName", [])
                self.considerError(lastError, None)
                return (_G_apply_1461, self.currentError)
            def _G_or_1462():
                self._trace('[head] + tail\n      ', (12176, 12196), self.input.position)
                _G_apply_1463, lastError = self._apply(self.rule_EscapedSymbolicName, "EscapedSymbolicName", [])
                self.considerError(lastError, None)
                return (_G_apply_1463, self.currentError)
            _G_or_1464, lastError = self._or([_G_or_1460, _G_or_1462])
            self.considerError(lastError, 'SymbolicName')
            return (_G_or_1464, self.currentError)


        def rule_UnescapedSymbolicName(self):
            _locals = {'self': self}
            self.locals['UnescapedSymbolicName'] = _locals
            def _G_consumedby_1465():
                self._trace('      ', (12223, 12229), self.input.position)
                _G_apply_1466, lastError = self._apply(self.rule_letter, "letter", [])
                self.considerError(lastError, None)
                def _G_many_1467():
                    def _G_or_1468():
                        self._trace('   ', (12231, 12234), self.input.position)
                        _G_exactly_1469, lastError = self.exactly('_')
                        self.considerError(lastError, None)
                        return (_G_exactly_1469, self.currentError)
                    def _G_or_1470():
                        self._trace('  \'}\' -> ["Lit', (12236, 12250), self.input.position)
                        _G_apply_1471, lastError = self._apply(self.rule_letterOrDigit, "letterOrDigit", [])
                        self.considerError(lastError, None)
                        return (_G_apply_1471, self.currentError)
                    _G_or_1472, lastError = self._or([_G_or_1468, _G_or_1470])
                    self.considerError(lastError, None)
                    return (_G_or_1472, self.currentError)
                _G_many_1473, lastError = self.many(_G_many_1467)
                self.considerError(lastError, None)
                return (_G_many_1473, self.currentError)
            _G_consumedby_1474, lastError = self.consumedby(_G_consumedby_1465)
            self.considerError(lastError, 'UnescapedSymbolicName')
            return (_G_consumedby_1474, self.currentError)


        def rule_EscapedSymbolicName(self):
            _locals = {'self': self}
            self.locals['EscapedSymbolicName'] = _locals
            self._trace('aram', (12276, 12280), self.input.position)
            _G_exactly_1475, lastError = self.exactly('`')
            self.considerError(lastError, 'EscapedSymbolicName')
            def _G_many_1476():
                def _G_or_1477():
                    def _G_not_1478():
                        self._trace('r =', (12283, 12286), self.input.position)
                        _G_exactly_1479, lastError = self.exactly('`')
                        self.considerError(lastError, None)
                        return (_G_exactly_1479, self.currentError)
                    _G_not_1480, lastError = self._not(_G_not_1478)
                    self.considerError(lastError, None)
                    self._trace(" '$' (Sym", (12286, 12295), self.input.position)
                    _G_apply_1481, lastError = self._apply(self.rule_anything, "anything", [])
                    self.considerError(lastError, None)
                    return (_G_apply_1481, self.currentError)
                def _G_or_1482():
                    self._trace('licNa', (12297, 12302), self.input.position)
                    _G_apply_1483, lastError = self._apply(self.rule_token, "token", ["``"])
                    self.considerError(lastError, None)
                    _G_python_1484, lastError = ('`'), None
                    self.considerError(lastError, None)
                    return (_G_python_1484, self.currentError)
                _G_or_1485, lastError = self._or([_G_or_1477, _G_or_1482])
                self.considerError(lastError, None)
                return (_G_or_1485, self.currentError)
            _G_many_1486, lastError = self.many(_G_many_1476)
            self.considerError(lastError, 'EscapedSymbolicName')
            _locals['cs'] = _G_many_1486
            self._trace('Inte', (12314, 12318), self.input.position)
            _G_exactly_1487, lastError = self.exactly('`')
            self.considerError(lastError, 'EscapedSymbolicName')
            _G_python_1488, lastError = eval(self._G_expr_1256, self.globals, _locals), None
            self.considerError(lastError, 'EscapedSymbolicName')
            return (_G_python_1488, self.currentError)


        def rule_WS(self):
            _locals = {'self': self}
            self.locals['WS'] = _locals
            def _G_many_1489():
                self._trace('", p]\n\n    ', (12339, 12350), self.input.position)
                _G_apply_1490, lastError = self._apply(self.rule_whitespace, "whitespace", [])
                self.considerError(lastError, None)
                return (_G_apply_1490, self.currentError)
            _G_many_1491, lastError = self.many(_G_many_1489)
            self.considerError(lastError, 'WS')
            return (_G_many_1491, self.currentError)


        def rule_SP(self):
            _locals = {'self': self}
            self.locals['SP'] = _locals
            def _G_many1_1492():
                self._trace('yExpression', (12357, 12368), self.input.position)
                _G_apply_1493, lastError = self._apply(self.rule_whitespace, "whitespace", [])
                self.considerError(lastError, None)
                return (_G_apply_1493, self.currentError)
            _G_many1_1494, lastError = self.many(_G_many1_1492, _G_many1_1492())
            self.considerError(lastError, 'SP')
            return (_G_many1_1494, self.currentError)


        def rule_whitespace(self):
            _locals = {'self': self}
            self.locals['whitespace'] = _locals
            def _G_or_1495():
                self._trace('rope', (12383, 12387), self.input.position)
                _G_exactly_1496, lastError = self.exactly(' ')
                self.considerError(lastError, None)
                return (_G_exactly_1496, self.currentError)
            def _G_or_1497():
                self._trace('pts -', (12400, 12405), self.input.position)
                _G_exactly_1498, lastError = self.exactly('\t')
                self.considerError(lastError, None)
                return (_G_exactly_1498, self.currentError)
            def _G_or_1499():
                self._trace('n", a', (12418, 12423), self.input.position)
                _G_exactly_1500, lastError = self.exactly('\n')
                self.considerError(lastError, None)
                return (_G_exactly_1500, self.currentError)
            def _G_or_1501():
                self._trace('Property', (12436, 12444), self.input.position)
                _G_apply_1502, lastError = self._apply(self.rule_Comment, "Comment", [])
                self.considerError(lastError, None)
                return (_G_apply_1502, self.currentError)
            _G_or_1503, lastError = self._or([_G_or_1495, _G_or_1497, _G_or_1499, _G_or_1501])
            self.considerError(lastError, 'whitespace')
            return (_G_or_1503, self.currentError)


        def rule_Comment(self):
            _locals = {'self': self}
            self.locals['Comment'] = _locals
            def _G_or_1504():
                self._trace('ymbol', (12455, 12460), self.input.position)
                _G_apply_1505, lastError = self._apply(self.rule_token, "token", ["/*"])
                self.considerError(lastError, None)
                def _G_many_1506():
                    def _G_not_1507():
                        self._trace('ame\n', (12463, 12467), self.input.position)
                        _G_apply_1508, lastError = self._apply(self.rule_token, "token", ["*/"])
                        self.considerError(lastError, None)
                        return (_G_apply_1508, self.currentError)
                    _G_not_1509, lastError = self._not(_G_not_1507)
                    self.considerError(lastError, None)
                    self._trace('\n    Inte', (12467, 12476), self.input.position)
                    _G_apply_1510, lastError = self._apply(self.rule_anything, "anything", [])
                    self.considerError(lastError, None)
                    return (_G_apply_1510, self.currentError)
                _G_many_1511, lastError = self.many(_G_many_1506)
                self.considerError(lastError, None)
                self._trace('rLite', (12478, 12483), self.input.position)
                _G_apply_1512, lastError = self._apply(self.rule_token, "token", ["*/"])
                self.considerError(lastError, None)
                return (_G_apply_1512, self.currentError)
            def _G_or_1513():
                self._trace('ntege', (12493, 12498), self.input.position)
                _G_apply_1514, lastError = self._apply(self.rule_token, "token", ["//"])
                self.considerError(lastError, None)
                def _G_many_1515():
                    def _G_not_1516():
                        def _G_or_1517():
                            self._trace('    ', (12502, 12506), self.input.position)
                            _G_exactly_1518, lastError = self.exactly('\r')
                            self.considerError(lastError, None)
                            return (_G_exactly_1518, self.currentError)
                        def _G_or_1519():
                            self._trace('    ', (12507, 12511), self.input.position)
                            _G_exactly_1520, lastError = self.exactly('\n')
                            self.considerError(lastError, None)
                            return (_G_exactly_1520, self.currentError)
                        _G_or_1521, lastError = self._or([_G_or_1517, _G_or_1519])
                        self.considerError(lastError, None)
                        return (_G_or_1521, self.currentError)
                    _G_not_1522, lastError = self._not(_G_not_1516)
                    self.considerError(lastError, None)
                    self._trace('       | ', (12512, 12521), self.input.position)
                    _G_apply_1523, lastError = self._apply(self.rule_anything, "anything", [])
                    self.considerError(lastError, None)
                    return (_G_apply_1523, self.currentError)
                _G_many_1524, lastError = self.many(_G_many_1515)
                self.considerError(lastError, None)
                def _G_optional_1525():
                    self._trace('talIn', (12523, 12528), self.input.position)
                    _G_exactly_1526, lastError = self.exactly('\r')
                    self.considerError(lastError, None)
                    return (_G_exactly_1526, self.currentError)
                def _G_optional_1527():
                    return (None, self.input.nullError())
                _G_or_1528, lastError = self._or([_G_optional_1525, _G_optional_1527])
                self.considerError(lastError, None)
                def _G_or_1529():
                    self._trace('er\n ', (12531, 12535), self.input.position)
                    _G_exactly_1530, lastError = self.exactly('\n')
                    self.considerError(lastError, None)
                    return (_G_exactly_1530, self.currentError)
                def _G_or_1531():
                    self._trace('   ', (12536, 12539), self.input.position)
                    _G_apply_1532, lastError = self._apply(self.rule_end, "end", [])
                    self.considerError(lastError, None)
                    return (_G_apply_1532, self.currentError)
                _G_or_1533, lastError = self._or([_G_or_1529, _G_or_1531])
                self.considerError(lastError, None)
                return (_G_or_1533, self.currentError)
            _G_or_1534, lastError = self._or([_G_or_1504, _G_or_1513])
            self.considerError(lastError, 'Comment')
            return (_G_or_1534, self.currentError)


        def rule_LeftArrowHead(self):
            _locals = {'self': self}
            self.locals['LeftArrowHead'] = _locals
            self._trace('cima', (12557, 12561), self.input.position)
            _G_exactly_1535, lastError = self.exactly('<')
            self.considerError(lastError, 'LeftArrowHead')
            return (_G_exactly_1535, self.currentError)


        def rule_RightArrowHead(self):
            _locals = {'self': self}
            self.locals['RightArrowHead'] = _locals
            self._trace('lDig', (12579, 12583), self.input.position)
            _G_exactly_1536, lastError = self.exactly('>')
            self.considerError(lastError, 'RightArrowHead')
            return (_G_exactly_1536, self.currentError)


        def rule_Dash(self):
            _locals = {'self': self}
            self.locals['Dash'] = _locals
            self._trace("8'|'", (12591, 12595), self.input.position)
            _G_exactly_1537, lastError = self.exactly('-')
            self.considerError(lastError, 'Dash')
            return (_G_exactly_1537, self.currentError)


        def rule_A(self):
            _locals = {'self': self}
            self.locals['A'] = _locals
            def _G_or_1538():
                self._trace('igit', (12600, 12604), self.input.position)
                _G_exactly_1539, lastError = self.exactly('A')
                self.considerError(lastError, None)
                return (_G_exactly_1539, self.currentError)
            def _G_or_1540():
                self._trace('    ', (12606, 12610), self.input.position)
                _G_exactly_1541, lastError = self.exactly('a')
                self.considerError(lastError, None)
                return (_G_exactly_1541, self.currentError)
            _G_or_1542, lastError = self._or([_G_or_1538, _G_or_1540])
            self.considerError(lastError, 'A')
            return (_G_or_1542, self.currentError)


        def rule_B(self):
            _locals = {'self': self}
            self.locals['B'] = _locals
            def _G_or_1543():
                self._trace('Inte', (12615, 12619), self.input.position)
                _G_exactly_1544, lastError = self.exactly('B')
                self.considerError(lastError, None)
                return (_G_exactly_1544, self.currentError)
            def _G_or_1545():
                self._trace('r = ', (12621, 12625), self.input.position)
                _G_exactly_1546, lastError = self.exactly('b')
                self.considerError(lastError, None)
                return (_G_exactly_1546, self.currentError)
            _G_or_1547, lastError = self._or([_G_or_1543, _G_or_1545])
            self.considerError(lastError, 'B')
            return (_G_or_1547, self.currentError)


        def rule_C(self):
            _locals = {'self': self}
            self.locals['C'] = _locals
            def _G_or_1548():
                self._trace('Octa', (12630, 12634), self.input.position)
                _G_exactly_1549, lastError = self.exactly('C')
                self.considerError(lastError, None)
                return (_G_exactly_1549, self.currentError)
            def _G_or_1550():
                self._trace('igit', (12636, 12640), self.input.position)
                _G_exactly_1551, lastError = self.exactly('c')
                self.considerError(lastError, None)
                return (_G_exactly_1551, self.currentError)
            _G_or_1552, lastError = self._or([_G_or_1548, _G_or_1550])
            self.considerError(lastError, 'C')
            return (_G_or_1552, self.currentError)


        def rule_D(self):
            _locals = {'self': self}
            self.locals['D'] = _locals
            def _G_or_1553():
                self._trace(' -> ', (12645, 12649), self.input.position)
                _G_exactly_1554, lastError = self.exactly('D')
                self.considerError(lastError, None)
                return (_G_exactly_1554, self.currentError)
            def _G_or_1555():
                self._trace('t(ds', (12651, 12655), self.input.position)
                _G_exactly_1556, lastError = self.exactly('d')
                self.considerError(lastError, None)
                return (_G_exactly_1556, self.currentError)
            _G_or_1557, lastError = self._or([_G_or_1553, _G_or_1555])
            self.considerError(lastError, 'D')
            return (_G_or_1557, self.currentError)


        def rule_E(self):
            _locals = {'self': self}
            self.locals['E'] = _locals
            def _G_or_1558():
                self._trace('\n   ', (12660, 12664), self.input.position)
                _G_exactly_1559, lastError = self.exactly('E')
                self.considerError(lastError, None)
                return (_G_exactly_1559, self.currentError)
            def _G_or_1560():
                self._trace('exDi', (12666, 12670), self.input.position)
                _G_exactly_1561, lastError = self.exactly('e')
                self.considerError(lastError, None)
                return (_G_exactly_1561, self.currentError)
            _G_or_1562, lastError = self._or([_G_or_1558, _G_or_1560])
            self.considerError(lastError, 'E')
            return (_G_or_1562, self.currentError)


        def rule_F(self):
            _locals = {'self': self}
            self.locals['F'] = _locals
            def _G_or_1563():
                self._trace(' dig', (12675, 12679), self.input.position)
                _G_exactly_1564, lastError = self.exactly('F')
                self.considerError(lastError, None)
                return (_G_exactly_1564, self.currentError)
            def _G_or_1565():
                self._trace(' | A', (12681, 12685), self.input.position)
                _G_exactly_1566, lastError = self.exactly('f')
                self.considerError(lastError, None)
                return (_G_exactly_1566, self.currentError)
            _G_or_1567, lastError = self._or([_G_or_1563, _G_or_1565])
            self.considerError(lastError, 'F')
            return (_G_or_1567, self.currentError)


        def rule_G(self):
            _locals = {'self': self}
            self.locals['G'] = _locals
            def _G_or_1568():
                self._trace('| C ', (12690, 12694), self.input.position)
                _G_exactly_1569, lastError = self.exactly('G')
                self.considerError(lastError, None)
                return (_G_exactly_1569, self.currentError)
            def _G_or_1570():
                self._trace('D | ', (12696, 12700), self.input.position)
                _G_exactly_1571, lastError = self.exactly('g')
                self.considerError(lastError, None)
                return (_G_exactly_1571, self.currentError)
            _G_or_1572, lastError = self._or([_G_or_1568, _G_or_1570])
            self.considerError(lastError, 'G')
            return (_G_or_1572, self.currentError)


        def rule_H(self):
            _locals = {'self': self}
            self.locals['H'] = _locals
            def _G_or_1573():
                self._trace('\n\n  ', (12705, 12709), self.input.position)
                _G_exactly_1574, lastError = self.exactly('H')
                self.considerError(lastError, None)
                return (_G_exactly_1574, self.currentError)
            def _G_or_1575():
                self._trace('HexI', (12711, 12715), self.input.position)
                _G_exactly_1576, lastError = self.exactly('h')
                self.considerError(lastError, None)
                return (_G_exactly_1576, self.currentError)
            _G_or_1577, lastError = self._or([_G_or_1573, _G_or_1575])
            self.considerError(lastError, 'H')
            return (_G_or_1577, self.currentError)


        def rule_I(self):
            _locals = {'self': self}
            self.locals['I'] = _locals
            def _G_or_1578():
                self._trace('r = ', (12720, 12724), self.input.position)
                _G_exactly_1579, lastError = self.exactly('I')
                self.considerError(lastError, None)
                return (_G_exactly_1579, self.currentError)
            def _G_or_1580():
                self._trace("' X ", (12726, 12730), self.input.position)
                _G_exactly_1581, lastError = self.exactly('i')
                self.considerError(lastError, None)
                return (_G_exactly_1581, self.currentError)
            _G_or_1582, lastError = self._or([_G_or_1578, _G_or_1580])
            self.considerError(lastError, 'I')
            return (_G_or_1582, self.currentError)


        def rule_K(self):
            _locals = {'self': self}
            self.locals['K'] = _locals
            def _G_or_1583():
                self._trace('igit', (12735, 12739), self.input.position)
                _G_exactly_1584, lastError = self.exactly('K')
                self.considerError(lastError, None)
                return (_G_exactly_1584, self.currentError)
            def _G_or_1585():
                self._trace(':ds ', (12741, 12745), self.input.position)
                _G_exactly_1586, lastError = self.exactly('k')
                self.considerError(lastError, None)
                return (_G_exactly_1586, self.currentError)
            _G_or_1587, lastError = self._or([_G_or_1583, _G_or_1585])
            self.considerError(lastError, 'K')
            return (_G_or_1587, self.currentError)


        def rule_L(self):
            _locals = {'self': self}
            self.locals['L'] = _locals
            def _G_or_1588():
                self._trace('t(ds', (12750, 12754), self.input.position)
                _G_exactly_1589, lastError = self.exactly('L')
                self.considerError(lastError, None)
                return (_G_exactly_1589, self.currentError)
            def _G_or_1590():
                self._trace('16)\n', (12756, 12760), self.input.position)
                _G_exactly_1591, lastError = self.exactly('l')
                self.considerError(lastError, None)
                return (_G_exactly_1591, self.currentError)
            _G_or_1592, lastError = self._or([_G_or_1588, _G_or_1590])
            self.considerError(lastError, 'L')
            return (_G_or_1592, self.currentError)


        def rule_M(self):
            _locals = {'self': self}
            self.locals['M'] = _locals
            def _G_or_1593():
                self._trace('Deci', (12765, 12769), self.input.position)
                _G_exactly_1594, lastError = self.exactly('M')
                self.considerError(lastError, None)
                return (_G_exactly_1594, self.currentError)
            def _G_or_1595():
                self._trace('lInt', (12771, 12775), self.input.position)
                _G_exactly_1596, lastError = self.exactly('m')
                self.considerError(lastError, None)
                return (_G_exactly_1596, self.currentError)
            _G_or_1597, lastError = self._or([_G_or_1593, _G_or_1595])
            self.considerError(lastError, 'M')
            return (_G_or_1597, self.currentError)


        def rule_N(self):
            _locals = {'self': self}
            self.locals['N'] = _locals
            def _G_or_1598():
                self._trace('= <d', (12780, 12784), self.input.position)
                _G_exactly_1599, lastError = self.exactly('N')
                self.considerError(lastError, None)
                return (_G_exactly_1599, self.currentError)
            def _G_or_1600():
                self._trace('it+>', (12786, 12790), self.input.position)
                _G_exactly_1601, lastError = self.exactly('n')
                self.considerError(lastError, None)
                return (_G_exactly_1601, self.currentError)
            _G_or_1602, lastError = self._or([_G_or_1598, _G_or_1600])
            self.considerError(lastError, 'N')
            return (_G_or_1602, self.currentError)


        def rule_O(self):
            _locals = {'self': self}
            self.locals['O'] = _locals
            def _G_or_1603():
                self._trace('> in', (12795, 12799), self.input.position)
                _G_exactly_1604, lastError = self.exactly('O')
                self.considerError(lastError, None)
                return (_G_exactly_1604, self.currentError)
            def _G_or_1605():
                self._trace('ds)\n', (12801, 12805), self.input.position)
                _G_exactly_1606, lastError = self.exactly('o')
                self.considerError(lastError, None)
                return (_G_exactly_1606, self.currentError)
            _G_or_1607, lastError = self._or([_G_or_1603, _G_or_1605])
            self.considerError(lastError, 'O')
            return (_G_or_1607, self.currentError)


        def rule_P(self):
            _locals = {'self': self}
            self.locals['P'] = _locals
            def _G_or_1608():
                self._trace('Doub', (12810, 12814), self.input.position)
                _G_exactly_1609, lastError = self.exactly('P')
                self.considerError(lastError, None)
                return (_G_exactly_1609, self.currentError)
            def _G_or_1610():
                self._trace('Lite', (12816, 12820), self.input.position)
                _G_exactly_1611, lastError = self.exactly('p')
                self.considerError(lastError, None)
                return (_G_exactly_1611, self.currentError)
            _G_or_1612, lastError = self._or([_G_or_1608, _G_or_1610])
            self.considerError(lastError, 'P')
            return (_G_or_1612, self.currentError)


        def rule_R(self):
            _locals = {'self': self}
            self.locals['R'] = _locals
            def _G_or_1613():
                self._trace(' Exp', (12825, 12829), self.input.position)
                _G_exactly_1614, lastError = self.exactly('R')
                self.considerError(lastError, None)
                return (_G_exactly_1614, self.currentError)
            def _G_or_1615():
                self._trace('entD', (12831, 12835), self.input.position)
                _G_exactly_1616, lastError = self.exactly('r')
                self.considerError(lastError, None)
                return (_G_exactly_1616, self.currentError)
            _G_or_1617, lastError = self._or([_G_or_1613, _G_or_1615])
            self.considerError(lastError, 'R')
            return (_G_or_1617, self.currentError)


        def rule_S(self):
            _locals = {'self': self}
            self.locals['S'] = _locals
            def _G_or_1618():
                self._trace('lRea', (12840, 12844), self.input.position)
                _G_exactly_1619, lastError = self.exactly('S')
                self.considerError(lastError, None)
                return (_G_exactly_1619, self.currentError)
            def _G_or_1620():
                self._trace('    ', (12846, 12850), self.input.position)
                _G_exactly_1621, lastError = self.exactly('s')
                self.considerError(lastError, None)
                return (_G_exactly_1621, self.currentError)
            _G_or_1622, lastError = self._or([_G_or_1618, _G_or_1620])
            self.considerError(lastError, 'S')
            return (_G_or_1622, self.currentError)


        def rule_T(self):
            _locals = {'self': self}
            self.locals['T'] = _locals
            def _G_or_1623():
                self._trace('    ', (12855, 12859), self.input.position)
                _G_exactly_1624, lastError = self.exactly('T')
                self.considerError(lastError, None)
                return (_G_exactly_1624, self.currentError)
            def _G_or_1625():
                self._trace('   |', (12861, 12865), self.input.position)
                _G_exactly_1626, lastError = self.exactly('t')
                self.considerError(lastError, None)
                return (_G_exactly_1626, self.currentError)
            _G_or_1627, lastError = self._or([_G_or_1623, _G_or_1625])
            self.considerError(lastError, 'T')
            return (_G_or_1627, self.currentError)


        def rule_U(self):
            _locals = {'self': self}
            self.locals['U'] = _locals
            def _G_or_1628():
                self._trace('larD', (12870, 12874), self.input.position)
                _G_exactly_1629, lastError = self.exactly('U')
                self.considerError(lastError, None)
                return (_G_exactly_1629, self.currentError)
            def _G_or_1630():
                self._trace('imal', (12876, 12880), self.input.position)
                _G_exactly_1631, lastError = self.exactly('u')
                self.considerError(lastError, None)
                return (_G_exactly_1631, self.currentError)
            _G_or_1632, lastError = self._or([_G_or_1628, _G_or_1630])
            self.considerError(lastError, 'U')
            return (_G_or_1632, self.currentError)


        def rule_V(self):
            _locals = {'self': self}
            self.locals['V'] = _locals
            def _G_or_1633():
                self._trace('\n   ', (12885, 12889), self.input.position)
                _G_exactly_1634, lastError = self.exactly('V')
                self.considerError(lastError, None)
                return (_G_exactly_1634, self.currentError)
            def _G_or_1635():
                self._trace('xpon', (12891, 12895), self.input.position)
                _G_exactly_1636, lastError = self.exactly('v')
                self.considerError(lastError, None)
                return (_G_exactly_1636, self.currentError)
            _G_or_1637, lastError = self._or([_G_or_1633, _G_or_1635])
            self.considerError(lastError, 'V')
            return (_G_or_1637, self.currentError)


        def rule_W(self):
            _locals = {'self': self}
            self.locals['W'] = _locals
            def _G_or_1638():
                self._trace('cima', (12900, 12904), self.input.position)
                _G_exactly_1639, lastError = self.exactly('W')
                self.considerError(lastError, None)
                return (_G_exactly_1639, self.currentError)
            def _G_or_1640():
                self._trace('eal ', (12906, 12910), self.input.position)
                _G_exactly_1641, lastError = self.exactly('w')
                self.considerError(lastError, None)
                return (_G_exactly_1641, self.currentError)
            _G_or_1642, lastError = self._or([_G_or_1638, _G_or_1640])
            self.considerError(lastError, 'W')
            return (_G_or_1642, self.currentError)


        def rule_X(self):
            _locals = {'self': self}
            self.locals['X'] = _locals
            def _G_or_1643():
                self._trace('egul', (12915, 12919), self.input.position)
                _G_exactly_1644, lastError = self.exactly('X')
                self.considerError(lastError, None)
                return (_G_exactly_1644, self.currentError)
            def _G_or_1645():
                self._trace('Deci', (12921, 12925), self.input.position)
                _G_exactly_1646, lastError = self.exactly('x')
                self.considerError(lastError, None)
                return (_G_exactly_1646, self.currentError)
            _G_or_1647, lastError = self._or([_G_or_1643, _G_or_1645])
            self.considerError(lastError, 'X')
            return (_G_or_1647, self.currentError)


        def rule_Y(self):
            _locals = {'self': self}
            self.locals['Y'] = _locals
            def _G_or_1648():
                self._trace('al |', (12930, 12934), self.input.position)
                _G_exactly_1649, lastError = self.exactly('Y')
                self.considerError(lastError, None)
                return (_G_exactly_1649, self.currentError)
            def _G_or_1650():
                self._trace('ecim', (12936, 12940), self.input.position)
                _G_exactly_1651, lastError = self.exactly('y')
                self.considerError(lastError, None)
                return (_G_exactly_1651, self.currentError)
            _G_or_1652, lastError = self._or([_G_or_1648, _G_or_1650])
            self.considerError(lastError, 'Y')
            return (_G_or_1652, self.currentError)


        def rule_Z(self):
            _locals = {'self': self}
            self.locals['Z'] = _locals
            def _G_or_1653():
                self._trace('eger', (12945, 12949), self.input.position)
                _G_exactly_1654, lastError = self.exactly('Z')
                self.considerError(lastError, None)
                return (_G_exactly_1654, self.currentError)
            def _G_or_1655():
                self._trace("E ('", (12951, 12955), self.input.position)
                _G_exactly_1656, lastError = self.exactly('z')
                self.considerError(lastError, None)
                return (_G_exactly_1656, self.currentError)
            _G_or_1657, lastError = self._or([_G_or_1653, _G_or_1655])
            self.considerError(lastError, 'Z')
            return (_G_or_1657, self.currentError)


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
        _G_expr_276 = compile('["With", d, rb, w]', '<string>', 'eval')
        _G_expr_298 = compile('["Return", d, rb]', '<string>', 'eval')
        _G_expr_316 = compile('["ReturnBody", ri, o, s, l]', '<string>', 'eval')
        _G_expr_329 = compile('["ReturnItems", [head] + tail]', '<string>', 'eval')
        _G_expr_338 = compile('["ReturnItem", ex, s]', '<string>', 'eval')
        _G_expr_342 = compile('["ReturnItem", ex, None]', '<string>', 'eval')
        _G_expr_361 = compile('["Order", [head] + tail]', '<string>', 'eval')
        _G_expr_369 = compile('["Skip", ex]', '<string>', 'eval')
        _G_expr_378 = compile('["Limit", ex]', '<string>', 'eval')
        _G_expr_401 = compile('["sort", ex, "desc"]', '<string>', 'eval')
        _G_expr_425 = compile('["sort", ex, "asc"]', '<string>', 'eval')
        _G_expr_435 = compile('["Where", ex]', '<string>', 'eval')
        _G_expr_443 = compile('[head] + tail', '<string>', 'eval')
        _G_expr_451 = compile('["PatternPart", v, ap]', '<string>', 'eval')
        _G_expr_458 = compile('["GraphPatternPart", v, ap]', '<string>', 'eval')
        _G_expr_462 = compile('["PatternPart", None, ap]', '<string>', 'eval')
        _G_expr_472 = compile('["PatternElement", np, pec]', '<string>', 'eval')
        _G_expr_478 = compile('pe', '<string>', 'eval')
        _G_expr_492 = compile('nl', '<string>', 'eval')
        _G_expr_499 = compile('p', '<string>', 'eval')
        _G_expr_504 = compile('["NodePattern", s, nl, p]', '<string>', 'eval')
        _G_expr_509 = compile('["PatternElementChain", rp, np]', '<string>', 'eval')
        _G_expr_529 = compile('["RelationshipsPattern", la, rd, ra]', '<string>', 'eval')
        _G_expr_555 = compile('["RelationshipDetail", v, q, rt, rl, p]', '<string>', 'eval')
        _G_expr_574 = compile('["RelationshipTypes", head] + tail', '<string>', 'eval')
        _G_expr_584 = compile('["NodeLabel", n]', '<string>', 'eval')
        _G_expr_599 = compile('slice(start, stop)', '<string>', 'eval')
        _G_expr_611 = compile('["or", ex1, ex2]', '<string>', 'eval')
        _G_expr_624 = compile('["xor", ex1, ex2]', '<string>', 'eval')
        _G_expr_637 = compile('["and", ex1, ex2]', '<string>', 'eval')
        _G_expr_648 = compile('["not", ex]', '<string>', 'eval')
        _G_expr_659 = compile('["eq",  ex1, ex2]', '<string>', 'eval')
        _G_expr_667 = compile('["neq", ex1, ex2]', '<string>', 'eval')
        _G_expr_682 = compile('["lt",  ex1, ex2]', '<string>', 'eval')
        _G_expr_690 = compile('["gt",  ex1, ex2]', '<string>', 'eval')
        _G_expr_698 = compile('["lte", ex1, ex2]', '<string>', 'eval')
        _G_expr_706 = compile('["gte", ex1, ex2]', '<string>', 'eval')
        _G_expr_717 = compile('["add", ex1, ex2]', '<string>', 'eval')
        _G_expr_725 = compile('["sub", ex1, ex2]', '<string>', 'eval')
        _G_expr_736 = compile('["multi", ex1, ex2]', '<string>', 'eval')
        _G_expr_744 = compile('["div",   ex1, ex2]', '<string>', 'eval')
        _G_expr_752 = compile('["mod",   ex1, ex2]', '<string>', 'eval')
        _G_expr_763 = compile('["hat", ex1, ex2]', '<string>', 'eval')
        _G_expr_776 = compile('["minus", ex]', '<string>', 'eval')
        _G_expr_789 = compile('["PropertyLookup", prop_name]', '<string>', 'eval')
        _G_expr_804 = compile('["slice", start, end]', '<string>', 'eval')
        _G_expr_856 = compile('[operator, ex2]', '<string>', 'eval')
        _G_expr_884 = compile('["Expression3", ex1, c]', '<string>', 'eval')
        _G_expr_898 = compile('["Expression2", a, c]', '<string>', 'eval')
        _G_expr_955 = compile('item', '<string>', 'eval')
        _G_expr_963 = compile('["List", ex]', '<string>', 'eval')
        _G_expr_978 = compile('["Filter", fex]', '<string>', 'eval')
        _G_expr_1000 = compile('["Extract", fex, ex]', '<string>', 'eval')
        _G_expr_1012 = compile('["All", fex]', '<string>', 'eval')
        _G_expr_1024 = compile('["Any", fex]', '<string>', 'eval')
        _G_expr_1037 = compile('["None", fex]', '<string>', 'eval')
        _G_expr_1052 = compile('["Single", fex]', '<string>', 'eval')
        _G_expr_1074 = compile('ex', '<string>', 'eval')
        _G_expr_1081 = compile('["ImplicitExistsExpression", [[\'PatternPart\', None, [\'PatternElement\', np, pec]]], None]', '<string>', 'eval')
        _G_expr_1091 = compile('["ImplicitExistsExpression", [[\'GraphPatternPart\', v, [\'PatternElement\', np, pec]]], None]', '<string>', 'eval')
        _G_expr_1110 = compile('["ExplicitExistsExpression", p, w]', '<string>', 'eval')
        _G_expr_1124 = compile('["ExistsFunction", p, None]', '<string>', 'eval')
        _G_expr_1132 = compile('["FilterExpression", i, w]', '<string>', 'eval')
        _G_expr_1140 = compile('["IdInColl", v, ex]', '<string>', 'eval')
        _G_expr_1172 = compile('["call", func, distinct, args]', '<string>', 'eval')
        _G_expr_1184 = compile('["ListComprehension", fex, ex]', '<string>', 'eval')
        _G_expr_1190 = compile('["PropertyLookup", n]', '<string>', 'eval')
        _G_expr_1219 = compile('["Case", ex, cas, el]', '<string>', 'eval')
        _G_expr_1234 = compile('[ex1, ex2]', '<string>', 'eval')
        _G_expr_1237 = compile('["Variable", s]', '<string>', 'eval')
        _G_expr_1256 = compile('"".join(cs)', '<string>', 'eval')
        _G_expr_1277 = compile('["Literal", l]', '<string>', 'eval')
        _G_expr_1319 = compile('(k, v)', '<string>', 'eval')
        _G_expr_1338 = compile('["Literal", dict(pairs)]', '<string>', 'eval')
        _G_expr_1346 = compile('["Parameter", p]', '<string>', 'eval')
        _G_expr_1353 = compile('["Expression", a, opts]', '<string>', 'eval')
        _G_expr_1377 = compile('int(ds, 8)', '<string>', 'eval')
        _G_expr_1401 = compile('int(ds, 16)', '<string>', 'eval')
        _G_expr_1408 = compile('int(ds)', '<string>', 'eval')
        _G_expr_1432 = compile('float(ds)', '<string>', 'eval')
    if Grammar.globals is not None:
        Grammar.globals = Grammar.globals.copy()
        Grammar.globals.update(ruleGlobals)
    else:
        Grammar.globals = ruleGlobals
    return Grammar