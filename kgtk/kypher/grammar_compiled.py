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


        def rule_Match(self):
            _locals = {'self': self}
            self.locals['Match'] = _locals
            def _G_optional_57():
                self._trace('m', (664, 665), self.input.position)
                _G_apply_58, lastError = self._apply(self.rule_O, "O", [])
                self.considerError(lastError, None)
                self._trace(', ', (665, 667), self.input.position)
                _G_apply_59, lastError = self._apply(self.rule_P, "P", [])
                self.considerError(lastError, None)
                self._trace('w,', (667, 669), self.input.position)
                _G_apply_60, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                self._trace(' r', (669, 671), self.input.position)
                _G_apply_61, lastError = self._apply(self.rule_I, "I", [])
                self.considerError(lastError, None)
                self._trace(']\n', (671, 673), self.input.position)
                _G_apply_62, lastError = self._apply(self.rule_O, "O", [])
                self.considerError(lastError, None)
                self._trace('\n ', (673, 675), self.input.position)
                _G_apply_63, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace('  ', (675, 677), self.input.position)
                _G_apply_64, lastError = self._apply(self.rule_A, "A", [])
                self.considerError(lastError, None)
                self._trace(' #', (677, 679), self.input.position)
                _G_apply_65, lastError = self._apply(self.rule_L, "L", [])
                self.considerError(lastError, None)
                self._trace(' TO', (679, 682), self.input.position)
                _G_apply_66, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                return (_G_apply_66, self.currentError)
            def _G_optional_67():
                return (None, self.input.nullError())
            _G_or_68, lastError = self._or([_G_optional_57, _G_optional_67])
            self.considerError(lastError, 'Match')
            self._trace(': ', (684, 686), self.input.position)
            _G_apply_69, lastError = self._apply(self.rule_M, "M", [])
            self.considerError(lastError, 'Match')
            self._trace('No', (686, 688), self.input.position)
            _G_apply_70, lastError = self._apply(self.rule_A, "A", [])
            self.considerError(lastError, 'Match')
            self._trace('t ', (688, 690), self.input.position)
            _G_apply_71, lastError = self._apply(self.rule_T, "T", [])
            self.considerError(lastError, 'Match')
            self._trace('su', (690, 692), self.input.position)
            _G_apply_72, lastError = self._apply(self.rule_C, "C", [])
            self.considerError(lastError, 'Match')
            self._trace('re', (692, 694), self.input.position)
            _G_apply_73, lastError = self._apply(self.rule_H, "H", [])
            self.considerError(lastError, 'Match')
            self._trace(' if', (694, 697), self.input.position)
            _G_apply_74, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'Match')
            self._trace(' I need ', (697, 705), self.input.position)
            _G_apply_75, lastError = self._apply(self.rule_Pattern, "Pattern", [])
            self.considerError(lastError, 'Match')
            _locals['p'] = _G_apply_75
            def _G_optional_76():
                self._trace('an', (709, 711), self.input.position)
                _G_apply_77, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('dle op', (711, 717), self.input.position)
                _G_apply_78, lastError = self._apply(self.rule_Where, "Where", [])
                self.considerError(lastError, None)
                return (_G_apply_78, self.currentError)
            def _G_optional_79():
                return (None, self.input.nullError())
            _G_or_80, lastError = self._or([_G_optional_76, _G_optional_79])
            self.considerError(lastError, 'Match')
            _locals['w'] = _G_or_80
            _G_python_82, lastError = eval(self._G_expr_81, self.globals, _locals), None
            self.considerError(lastError, 'Match')
            return (_G_python_82, self.currentError)


        def rule_Unwind(self):
            _locals = {'self': self}
            self.locals['Unwind'] = _locals
            self._trace('N ', (750, 752), self.input.position)
            _G_apply_83, lastError = self._apply(self.rule_U, "U", [])
            self.considerError(lastError, 'Unwind')
            self._trace('A ', (752, 754), self.input.position)
            _G_apply_84, lastError = self._apply(self.rule_N, "N", [])
            self.considerError(lastError, 'Unwind')
            self._trace('L ', (754, 756), self.input.position)
            _G_apply_85, lastError = self._apply(self.rule_W, "W", [])
            self.considerError(lastError, 'Unwind')
            self._trace('SP', (756, 758), self.input.position)
            _G_apply_86, lastError = self._apply(self.rule_I, "I", [])
            self.considerError(lastError, 'Unwind')
            self._trace(')?', (758, 760), self.input.position)
            _G_apply_87, lastError = self._apply(self.rule_N, "N", [])
            self.considerError(lastError, 'Unwind')
            self._trace(' M', (760, 762), self.input.position)
            _G_apply_88, lastError = self._apply(self.rule_D, "D", [])
            self.considerError(lastError, 'Unwind')
            self._trace(' A ', (762, 765), self.input.position)
            _G_apply_89, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'Unwind')
            self._trace('T C H WS Pa', (765, 776), self.input.position)
            _G_apply_90, lastError = self._apply(self.rule_Expression, "Expression", [])
            self.considerError(lastError, 'Unwind')
            _locals['ex'] = _G_apply_90
            self._trace('rn:', (779, 782), self.input.position)
            _G_apply_91, lastError = self._apply(self.rule_SP, "SP", [])
            self.considerError(lastError, 'Unwind')
            self._trace('p ', (782, 784), self.input.position)
            _G_apply_92, lastError = self._apply(self.rule_A, "A", [])
            self.considerError(lastError, 'Unwind')
            self._trace('(W', (784, 786), self.input.position)
            _G_apply_93, lastError = self._apply(self.rule_S, "S", [])
            self.considerError(lastError, 'Unwind')
            self._trace('S W', (786, 789), self.input.position)
            _G_apply_94, lastError = self._apply(self.rule_SP, "SP", [])
            self.considerError(lastError, 'Unwind')
            self._trace('here)?:w ', (789, 798), self.input.position)
            _G_apply_95, lastError = self._apply(self.rule_Variable, "Variable", [])
            self.considerError(lastError, 'Unwind')
            _locals['v'] = _G_apply_95
            _G_python_97, lastError = eval(self._G_expr_96, self.globals, _locals), None
            self.considerError(lastError, 'Unwind')
            return (_G_python_97, self.currentError)


        def rule_Merge(self):
            _locals = {'self': self}
            self.locals['Merge'] = _locals
            self._trace(' U', (830, 832), self.input.position)
            _G_apply_98, lastError = self._apply(self.rule_M, "M", [])
            self.considerError(lastError, 'Merge')
            self._trace(' N', (832, 834), self.input.position)
            _G_apply_99, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'Merge')
            self._trace(' W', (834, 836), self.input.position)
            _G_apply_100, lastError = self._apply(self.rule_R, "R", [])
            self.considerError(lastError, 'Merge')
            self._trace(' I', (836, 838), self.input.position)
            _G_apply_101, lastError = self._apply(self.rule_G, "G", [])
            self.considerError(lastError, 'Merge')
            self._trace(' N', (838, 840), self.input.position)
            _G_apply_102, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'Merge')
            self._trace(' D ', (840, 843), self.input.position)
            _G_apply_103, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'Merge')
            self._trace('WS Expressio', (843, 855), self.input.position)
            _G_apply_104, lastError = self._apply(self.rule_PatternPart, "PatternPart", [])
            self.considerError(lastError, 'Merge')
            _locals['head'] = _G_apply_104
            def _G_many_105():
                self._trace(' A', (862, 864), self.input.position)
                _G_apply_106, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace(' S SP Variab', (864, 876), self.input.position)
                _G_apply_107, lastError = self._apply(self.rule_MergeAction, "MergeAction", [])
                self.considerError(lastError, None)
                return (_G_apply_107, self.currentError)
            _G_many_108, lastError = self.many(_G_many_105)
            self.considerError(lastError, 'Merge')
            _locals['tail'] = _G_many_108
            _G_python_110, lastError = eval(self._G_expr_109, self.globals, _locals), None
            self.considerError(lastError, 'Merge')
            return (_G_python_110, self.currentError)


        def rule_MergeAction(self):
            _locals = {'self': self}
            self.locals['MergeAction'] = _locals
            def _G_or_111():
                self._trace('S ', (926, 928), self.input.position)
                _G_apply_112, lastError = self._apply(self.rule_O, "O", [])
                self.considerError(lastError, None)
                self._trace('Pa', (928, 930), self.input.position)
                _G_apply_113, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace('tte', (930, 933), self.input.position)
                _G_apply_114, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('rn', (933, 935), self.input.position)
                _G_apply_115, lastError = self._apply(self.rule_M, "M", [])
                self.considerError(lastError, None)
                self._trace('Pa', (935, 937), self.input.position)
                _G_apply_116, lastError = self._apply(self.rule_A, "A", [])
                self.considerError(lastError, None)
                self._trace('rt', (937, 939), self.input.position)
                _G_apply_117, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                self._trace(':h', (939, 941), self.input.position)
                _G_apply_118, lastError = self._apply(self.rule_C, "C", [])
                self.considerError(lastError, None)
                self._trace('ea', (941, 943), self.input.position)
                _G_apply_119, lastError = self._apply(self.rule_H, "H", [])
                self.considerError(lastError, None)
                self._trace('d (', (943, 946), self.input.position)
                _G_apply_120, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('SP M', (946, 950), self.input.position)
                _G_apply_121, lastError = self._apply(self.rule_Set, "Set", [])
                self.considerError(lastError, None)
                _locals['s'] = _G_apply_121
                _G_python_123, lastError = eval(self._G_expr_122, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_123, self.currentError)
            def _G_or_124():
                self._trace('l]', (993, 995), self.input.position)
                _G_apply_125, lastError = self._apply(self.rule_O, "O", [])
                self.considerError(lastError, None)
                self._trace('\n\n', (995, 997), self.input.position)
                _G_apply_126, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace('   ', (997, 1000), self.input.position)
                _G_apply_127, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace(' M', (1000, 1002), self.input.position)
                _G_apply_128, lastError = self._apply(self.rule_C, "C", [])
                self.considerError(lastError, None)
                self._trace('er', (1002, 1004), self.input.position)
                _G_apply_129, lastError = self._apply(self.rule_R, "R", [])
                self.considerError(lastError, None)
                self._trace('ge', (1004, 1006), self.input.position)
                _G_apply_130, lastError = self._apply(self.rule_E, "E", [])
                self.considerError(lastError, None)
                self._trace('Ac', (1006, 1008), self.input.position)
                _G_apply_131, lastError = self._apply(self.rule_A, "A", [])
                self.considerError(lastError, None)
                self._trace('ti', (1008, 1010), self.input.position)
                _G_apply_132, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                self._trace('on', (1010, 1012), self.input.position)
                _G_apply_133, lastError = self._apply(self.rule_E, "E", [])
                self.considerError(lastError, None)
                self._trace(' = ', (1012, 1015), self.input.position)
                _G_apply_134, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('O N ', (1015, 1019), self.input.position)
                _G_apply_135, lastError = self._apply(self.rule_Set, "Set", [])
                self.considerError(lastError, None)
                _locals['s'] = _G_apply_135
                _G_python_137, lastError = eval(self._G_expr_136, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_137, self.currentError)
            _G_or_138, lastError = self._or([_G_or_111, _G_or_124])
            self.considerError(lastError, 'MergeAction')
            return (_G_or_138, self.currentError)


        def rule_Create(self):
            _locals = {'self': self}
            self.locals['Create'] = _locals
            self._trace('tc', (1059, 1061), self.input.position)
            _G_apply_139, lastError = self._apply(self.rule_C, "C", [])
            self.considerError(lastError, 'Create')
            self._trace('h"', (1061, 1063), self.input.position)
            _G_apply_140, lastError = self._apply(self.rule_R, "R", [])
            self.considerError(lastError, 'Create')
            self._trace(', ', (1063, 1065), self.input.position)
            _G_apply_141, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'Create')
            self._trace('s]', (1065, 1067), self.input.position)
            _G_apply_142, lastError = self._apply(self.rule_A, "A", [])
            self.considerError(lastError, 'Create')
            self._trace('\n ', (1067, 1069), self.input.position)
            _G_apply_143, lastError = self._apply(self.rule_T, "T", [])
            self.considerError(lastError, 'Create')
            self._trace('  ', (1069, 1071), self.input.position)
            _G_apply_144, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'Create')
            self._trace('   ', (1071, 1074), self.input.position)
            _G_apply_145, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'Create')
            self._trace('        ', (1074, 1082), self.input.position)
            _G_apply_146, lastError = self._apply(self.rule_Pattern, "Pattern", [])
            self.considerError(lastError, 'Create')
            _locals['p'] = _G_apply_146
            _G_python_148, lastError = eval(self._G_expr_147, self.globals, _locals), None
            self.considerError(lastError, 'Create')
            return (_G_python_148, self.currentError)


        def rule_Set(self):
            _locals = {'self': self}
            self.locals['Set'] = _locals
            self._trace('Se', (1108, 1110), self.input.position)
            _G_apply_149, lastError = self._apply(self.rule_S, "S", [])
            self.considerError(lastError, 'Set')
            self._trace('t:', (1110, 1112), self.input.position)
            _G_apply_150, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'Set')
            self._trace('s ', (1112, 1114), self.input.position)
            _G_apply_151, lastError = self._apply(self.rule_T, "T", [])
            self.considerError(lastError, 'Set')
            self._trace('-> ', (1114, 1117), self.input.position)
            _G_apply_152, lastError = self._apply(self.rule_SP, "SP", [])
            self.considerError(lastError, 'Set')
            self._trace('["MergeA', (1117, 1125), self.input.position)
            _G_apply_153, lastError = self._apply(self.rule_SetItem, "SetItem", [])
            self.considerError(lastError, 'Set')
            _locals['head'] = _G_apply_153
            def _G_many_154():
                self._trace('ea', (1132, 1134), self.input.position)
                _G_apply_155, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('te",', (1134, 1138), self.input.position)
                _G_exactly_156, lastError = self.exactly(',')
                self.considerError(lastError, None)
                self._trace(' s]', (1138, 1141), self.input.position)
                _G_apply_157, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('\n\n    Cr', (1141, 1149), self.input.position)
                _G_apply_158, lastError = self._apply(self.rule_SetItem, "SetItem", [])
                self.considerError(lastError, None)
                return (_G_apply_158, self.currentError)
            _G_many_159, lastError = self.many(_G_many_154)
            self.considerError(lastError, 'Set')
            _locals['tail'] = _G_many_159
            _G_python_161, lastError = eval(self._G_expr_160, self.globals, _locals), None
            self.considerError(lastError, 'Set')
            return (_G_python_161, self.currentError)


        def rule_SetItem(self):
            _locals = {'self': self}
            self.locals['SetItem'] = _locals
            def _G_or_162():
                self._trace(', p]\n\n    Set = S E', (1193, 1212), self.input.position)
                _G_apply_163, lastError = self._apply(self.rule_PropertyExpression, "PropertyExpression", [])
                self.considerError(lastError, None)
                _locals['pex'] = _G_apply_163
                self._trace('P Se', (1216, 1220), self.input.position)
                _G_exactly_164, lastError = self.exactly('=')
                self.considerError(lastError, None)
                self._trace('tItem:head ', (1220, 1231), self.input.position)
                _G_apply_165, lastError = self._apply(self.rule_Expression, "Expression", [])
                self.considerError(lastError, None)
                _locals['ex'] = _G_apply_165
                _G_python_167, lastError = eval(self._G_expr_166, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_167, self.currentError)
            def _G_or_168():
                self._trace('  SetItem', (1286, 1295), self.input.position)
                _G_apply_169, lastError = self._apply(self.rule_Variable, "Variable", [])
                self.considerError(lastError, None)
                _locals['v'] = _G_apply_169
                self._trace(' Pro', (1297, 1301), self.input.position)
                _G_exactly_170, lastError = self.exactly('=')
                self.considerError(lastError, None)
                self._trace('pertyExpres', (1301, 1312), self.input.position)
                _G_apply_171, lastError = self._apply(self.rule_Expression, "Expression", [])
                self.considerError(lastError, None)
                _locals['ex'] = _G_apply_171
                _G_python_173, lastError = eval(self._G_expr_172, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_173, self.currentError)
            def _G_or_174():
                self._trace('ItemPrope', (1347, 1356), self.input.position)
                _G_apply_175, lastError = self._apply(self.rule_Variable, "Variable", [])
                self.considerError(lastError, None)
                _locals['v'] = _G_apply_175
                self._trace('yExpr', (1358, 1363), self.input.position)
                _G_exactly_176, lastError = self.exactly('+=')
                self.considerError(lastError, None)
                self._trace('ession", pe', (1363, 1374), self.input.position)
                _G_apply_177, lastError = self._apply(self.rule_Expression, "Expression", [])
                self.considerError(lastError, None)
                _locals['ex'] = _G_apply_177
                _G_python_178, lastError = eval(self._G_expr_172, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_178, self.currentError)
            def _G_or_179():
                self._trace(' Expressi', (1409, 1418), self.input.position)
                _G_apply_180, lastError = self._apply(self.rule_Variable, "Variable", [])
                self.considerError(lastError, None)
                _locals['v'] = _G_apply_180
                self._trace(':ex -> ["Se', (1420, 1431), self.input.position)
                _G_apply_181, lastError = self._apply(self.rule_NodeLabels, "NodeLabels", [])
                self.considerError(lastError, None)
                _locals['ex'] = _G_apply_181
                _G_python_182, lastError = eval(self._G_expr_172, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_182, self.currentError)
            _G_or_183, lastError = self._or([_G_or_162, _G_or_168, _G_or_174, _G_or_179])
            self.considerError(lastError, 'SetItem')
            return (_G_or_183, self.currentError)


        def rule_Delete(self):
            _locals = {'self': self}
            self.locals['Delete'] = _locals
            def _G_optional_184():
                self._trace(':', (1468, 1469), self.input.position)
                _G_apply_185, lastError = self._apply(self.rule_D, "D", [])
                self.considerError(lastError, None)
                self._trace('v ', (1469, 1471), self.input.position)
                _G_apply_186, lastError = self._apply(self.rule_E, "E", [])
                self.considerError(lastError, None)
                self._trace("'+", (1471, 1473), self.input.position)
                _G_apply_187, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                self._trace("='", (1473, 1475), self.input.position)
                _G_apply_188, lastError = self._apply(self.rule_A, "A", [])
                self.considerError(lastError, None)
                self._trace(' E', (1475, 1477), self.input.position)
                _G_apply_189, lastError = self._apply(self.rule_C, "C", [])
                self.considerError(lastError, None)
                self._trace('xp', (1477, 1479), self.input.position)
                _G_apply_190, lastError = self._apply(self.rule_H, "H", [])
                self.considerError(lastError, None)
                self._trace('res', (1479, 1482), self.input.position)
                _G_apply_191, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                return (_G_apply_191, self.currentError)
            def _G_optional_192():
                return (None, self.input.nullError())
            _G_or_193, lastError = self._or([_G_optional_184, _G_optional_192])
            self.considerError(lastError, 'Delete')
            self._trace('on', (1484, 1486), self.input.position)
            _G_apply_194, lastError = self._apply(self.rule_D, "D", [])
            self.considerError(lastError, 'Delete')
            self._trace(':e', (1486, 1488), self.input.position)
            _G_apply_195, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'Delete')
            self._trace('x ', (1488, 1490), self.input.position)
            _G_apply_196, lastError = self._apply(self.rule_L, "L", [])
            self.considerError(lastError, 'Delete')
            self._trace('->', (1490, 1492), self.input.position)
            _G_apply_197, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'Delete')
            self._trace(' [', (1492, 1494), self.input.position)
            _G_apply_198, lastError = self._apply(self.rule_T, "T", [])
            self.considerError(lastError, 'Delete')
            self._trace('"S', (1494, 1496), self.input.position)
            _G_apply_199, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'Delete')
            self._trace('etI', (1496, 1499), self.input.position)
            _G_apply_200, lastError = self._apply(self.rule_SP, "SP", [])
            self.considerError(lastError, 'Delete')
            self._trace('tem", v, ex', (1499, 1510), self.input.position)
            _G_apply_201, lastError = self._apply(self.rule_Expression, "Expression", [])
            self.considerError(lastError, 'Delete')
            _locals['head'] = _G_apply_201
            def _G_many_202():
                self._trace('   ', (1517, 1520), self.input.position)
                _G_exactly_203, lastError = self.exactly(',')
                self.considerError(lastError, None)
                self._trace('   ', (1520, 1523), self.input.position)
                _G_apply_204, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace(' | Variable', (1523, 1534), self.input.position)
                _G_apply_205, lastError = self._apply(self.rule_Expression, "Expression", [])
                self.considerError(lastError, None)
                return (_G_apply_205, self.currentError)
            _G_many_206, lastError = self.many(_G_many_202)
            self.considerError(lastError, 'Delete')
            _locals['tail'] = _G_many_206
            _G_python_208, lastError = eval(self._G_expr_207, self.globals, _locals), None
            self.considerError(lastError, 'Delete')
            return (_G_python_208, self.currentError)


        def rule_Remove(self):
            _locals = {'self': self}
            self.locals['Remove'] = _locals
            self._trace('et', (1581, 1583), self.input.position)
            _G_apply_209, lastError = self._apply(self.rule_R, "R", [])
            self.considerError(lastError, 'Remove')
            self._trace('e ', (1583, 1585), self.input.position)
            _G_apply_210, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'Remove')
            self._trace('= ', (1585, 1587), self.input.position)
            _G_apply_211, lastError = self._apply(self.rule_M, "M", [])
            self.considerError(lastError, 'Remove')
            self._trace('(D', (1587, 1589), self.input.position)
            _G_apply_212, lastError = self._apply(self.rule_O, "O", [])
            self.considerError(lastError, 'Remove')
            self._trace(' E', (1589, 1591), self.input.position)
            _G_apply_213, lastError = self._apply(self.rule_V, "V", [])
            self.considerError(lastError, 'Remove')
            self._trace(' T', (1591, 1593), self.input.position)
            _G_apply_214, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'Remove')
            self._trace(' A ', (1593, 1596), self.input.position)
            _G_apply_215, lastError = self._apply(self.rule_SP, "SP", [])
            self.considerError(lastError, 'Remove')
            self._trace('C H SP)? D ', (1596, 1607), self.input.position)
            _G_apply_216, lastError = self._apply(self.rule_RemoveItem, "RemoveItem", [])
            self.considerError(lastError, 'Remove')
            _locals['head'] = _G_apply_216
            def _G_many_217():
                self._trace(' E', (1614, 1616), self.input.position)
                _G_apply_218, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace(' SP ', (1616, 1620), self.input.position)
                _G_exactly_219, lastError = self.exactly(',')
                self.considerError(lastError, None)
                self._trace('Exp', (1620, 1623), self.input.position)
                _G_apply_220, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('ression:hea', (1623, 1634), self.input.position)
                _G_apply_221, lastError = self._apply(self.rule_RemoveItem, "RemoveItem", [])
                self.considerError(lastError, None)
                return (_G_apply_221, self.currentError)
            _G_many_222, lastError = self.many(_G_many_217)
            self.considerError(lastError, 'Remove')
            _locals['tail'] = _G_many_222
            _G_python_224, lastError = eval(self._G_expr_223, self.globals, _locals), None
            self.considerError(lastError, 'Remove')
            return (_G_python_224, self.currentError)


        def rule_RemoveItem(self):
            _locals = {'self': self}
            self.locals['RemoveItem'] = _locals
            def _G_or_225():
                self._trace('+ tail]\n\n', (1684, 1693), self.input.position)
                _G_apply_226, lastError = self._apply(self.rule_Variable, "Variable", [])
                self.considerError(lastError, None)
                _locals['v'] = _G_apply_226
                self._trace('  Remove = ', (1695, 1706), self.input.position)
                _G_apply_227, lastError = self._apply(self.rule_NodeLabels, "NodeLabels", [])
                self.considerError(lastError, None)
                _locals['nl'] = _G_apply_227
                _G_python_229, lastError = eval(self._G_expr_228, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_229, self.currentError)
            def _G_or_230():
                self._trace('oveItem)*:tail -> [', (1751, 1770), self.input.position)
                _G_apply_231, lastError = self._apply(self.rule_PropertyExpression, "PropertyExpression", [])
                self.considerError(lastError, None)
                _locals['p'] = _G_apply_231
                _G_python_233, lastError = eval(self._G_expr_232, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_233, self.currentError)
            _G_or_234, lastError = self._or([_G_or_225, _G_or_230])
            self.considerError(lastError, 'RemoveItem')
            return (_G_or_234, self.currentError)


        def rule_With(self):
            _locals = {'self': self}
            self.locals['With'] = _locals
            self._trace('ov', (1803, 1805), self.input.position)
            _G_apply_235, lastError = self._apply(self.rule_W, "W", [])
            self.considerError(lastError, 'With')
            self._trace('eI', (1805, 1807), self.input.position)
            _G_apply_236, lastError = self._apply(self.rule_I, "I", [])
            self.considerError(lastError, 'With')
            self._trace('te', (1807, 1809), self.input.position)
            _G_apply_237, lastError = self._apply(self.rule_T, "T", [])
            self.considerError(lastError, 'With')
            self._trace('m ', (1809, 1811), self.input.position)
            _G_apply_238, lastError = self._apply(self.rule_H, "H", [])
            self.considerError(lastError, 'With')
            def _G_optional_239():
                self._trace('Va', (1813, 1815), self.input.position)
                _G_apply_240, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('ri', (1815, 1817), self.input.position)
                _G_apply_241, lastError = self._apply(self.rule_D, "D", [])
                self.considerError(lastError, None)
                self._trace('ab', (1817, 1819), self.input.position)
                _G_apply_242, lastError = self._apply(self.rule_I, "I", [])
                self.considerError(lastError, None)
                self._trace('le', (1819, 1821), self.input.position)
                _G_apply_243, lastError = self._apply(self.rule_S, "S", [])
                self.considerError(lastError, None)
                self._trace(':v', (1821, 1823), self.input.position)
                _G_apply_244, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                self._trace(' N', (1823, 1825), self.input.position)
                _G_apply_245, lastError = self._apply(self.rule_I, "I", [])
                self.considerError(lastError, None)
                self._trace('od', (1825, 1827), self.input.position)
                _G_apply_246, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace('eL', (1827, 1829), self.input.position)
                _G_apply_247, lastError = self._apply(self.rule_C, "C", [])
                self.considerError(lastError, None)
                self._trace('ab', (1829, 1831), self.input.position)
                _G_apply_248, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                return (_G_apply_248, self.currentError)
            def _G_optional_249():
                return (None, self.input.nullError())
            _G_or_250, lastError = self._or([_G_optional_239, _G_optional_249])
            self.considerError(lastError, 'With')
            _locals['d'] = _G_or_250
            self._trace('nl ', (1835, 1838), self.input.position)
            _G_apply_251, lastError = self._apply(self.rule_SP, "SP", [])
            self.considerError(lastError, 'With')
            self._trace('-> ["Remove', (1838, 1849), self.input.position)
            _G_apply_252, lastError = self._apply(self.rule_ReturnBody, "ReturnBody", [])
            self.considerError(lastError, 'With')
            _locals['rb'] = _G_apply_252
            def _G_optional_253():
                self._trace('ar", ', (1854, 1859), self.input.position)
                _G_apply_254, lastError = self._apply(self.rule_Where, "Where", [])
                self.considerError(lastError, None)
                return (_G_apply_254, self.currentError)
            def _G_optional_255():
                return (None, self.input.nullError())
            _G_or_256, lastError = self._or([_G_optional_253, _G_optional_255])
            self.considerError(lastError, 'With')
            _locals['w'] = _G_or_256
            _G_python_258, lastError = eval(self._G_expr_257, self.globals, _locals), None
            self.considerError(lastError, 'With')
            return (_G_python_258, self.currentError)


        def rule_Return(self):
            _locals = {'self': self}
            self.locals['Return'] = _locals
            self._trace('re', (1895, 1897), self.input.position)
            _G_apply_259, lastError = self._apply(self.rule_R, "R", [])
            self.considerError(lastError, 'Return')
            self._trace('ss', (1897, 1899), self.input.position)
            _G_apply_260, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'Return')
            self._trace('io', (1899, 1901), self.input.position)
            _G_apply_261, lastError = self._apply(self.rule_T, "T", [])
            self.considerError(lastError, 'Return')
            self._trace('n:', (1901, 1903), self.input.position)
            _G_apply_262, lastError = self._apply(self.rule_U, "U", [])
            self.considerError(lastError, 'Return')
            self._trace('p ', (1903, 1905), self.input.position)
            _G_apply_263, lastError = self._apply(self.rule_R, "R", [])
            self.considerError(lastError, 'Return')
            self._trace('->', (1905, 1907), self.input.position)
            _G_apply_264, lastError = self._apply(self.rule_N, "N", [])
            self.considerError(lastError, 'Return')
            def _G_optional_265():
                self._trace('"R', (1909, 1911), self.input.position)
                _G_apply_266, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('em', (1911, 1913), self.input.position)
                _G_apply_267, lastError = self._apply(self.rule_D, "D", [])
                self.considerError(lastError, None)
                self._trace('ov', (1913, 1915), self.input.position)
                _G_apply_268, lastError = self._apply(self.rule_I, "I", [])
                self.considerError(lastError, None)
                self._trace('eI', (1915, 1917), self.input.position)
                _G_apply_269, lastError = self._apply(self.rule_S, "S", [])
                self.considerError(lastError, None)
                self._trace('te', (1917, 1919), self.input.position)
                _G_apply_270, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                self._trace('mP', (1919, 1921), self.input.position)
                _G_apply_271, lastError = self._apply(self.rule_I, "I", [])
                self.considerError(lastError, None)
                self._trace('e"', (1921, 1923), self.input.position)
                _G_apply_272, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace(', ', (1923, 1925), self.input.position)
                _G_apply_273, lastError = self._apply(self.rule_C, "C", [])
                self.considerError(lastError, None)
                self._trace('p]', (1925, 1927), self.input.position)
                _G_apply_274, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                return (_G_apply_274, self.currentError)
            def _G_optional_275():
                return (None, self.input.nullError())
            _G_or_276, lastError = self._or([_G_optional_265, _G_optional_275])
            self.considerError(lastError, 'Return')
            _locals['d'] = _G_or_276
            self._trace('  W', (1931, 1934), self.input.position)
            _G_apply_277, lastError = self._apply(self.rule_SP, "SP", [])
            self.considerError(lastError, 'Return')
            self._trace('ith = W I T', (1934, 1945), self.input.position)
            _G_apply_278, lastError = self._apply(self.rule_ReturnBody, "ReturnBody", [])
            self.considerError(lastError, 'Return')
            _locals['rb'] = _G_apply_278
            _G_python_280, lastError = eval(self._G_expr_279, self.globals, _locals), None
            self.considerError(lastError, 'Return')
            return (_G_python_280, self.currentError)


        def rule_ReturnBody(self):
            _locals = {'self': self}
            self.locals['ReturnBody'] = _locals
            self._trace('dy:rb (Where', (1983, 1995), self.input.position)
            _G_apply_281, lastError = self._apply(self.rule_ReturnItems, "ReturnItems", [])
            self.considerError(lastError, 'ReturnBody')
            _locals['ri'] = _G_apply_281
            def _G_optional_282():
                self._trace('->', (2000, 2002), self.input.position)
                _G_apply_283, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace(' ["Wit', (2002, 2008), self.input.position)
                _G_apply_284, lastError = self._apply(self.rule_Order, "Order", [])
                self.considerError(lastError, None)
                return (_G_apply_284, self.currentError)
            def _G_optional_285():
                return (None, self.input.nullError())
            _G_or_286, lastError = self._or([_G_optional_282, _G_optional_285])
            self.considerError(lastError, 'ReturnBody')
            _locals['o'] = _G_or_286
            def _G_optional_287():
                self._trace(' r', (2014, 2016), self.input.position)
                _G_apply_288, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('b, w]', (2016, 2021), self.input.position)
                _G_apply_289, lastError = self._apply(self.rule_Skip, "Skip", [])
                self.considerError(lastError, None)
                return (_G_apply_289, self.currentError)
            def _G_optional_290():
                return (None, self.input.nullError())
            _G_or_291, lastError = self._or([_G_optional_287, _G_optional_290])
            self.considerError(lastError, 'ReturnBody')
            _locals['s'] = _G_or_291
            def _G_optional_292():
                self._trace('Re', (2027, 2029), self.input.position)
                _G_apply_293, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('turn =', (2029, 2035), self.input.position)
                _G_apply_294, lastError = self._apply(self.rule_Limit, "Limit", [])
                self.considerError(lastError, None)
                return (_G_apply_294, self.currentError)
            def _G_optional_295():
                return (None, self.input.nullError())
            _G_or_296, lastError = self._or([_G_optional_292, _G_optional_295])
            self.considerError(lastError, 'ReturnBody')
            _locals['l'] = _G_or_296
            _G_python_298, lastError = eval(self._G_expr_297, self.globals, _locals), None
            self.considerError(lastError, 'ReturnBody')
            return (_G_python_298, self.currentError)


        def rule_ReturnItems(self):
            _locals = {'self': self}
            self.locals['ReturnItems'] = _locals
            def _G_or_299():
                self._trace('b -', (2087, 2090), self.input.position)
                _G_exactly_300, lastError = self.exactly('*')
                self.considerError(lastError, None)
                return (_G_exactly_300, self.currentError)
            def _G_or_301():
                self._trace('["Return", ', (2092, 2103), self.input.position)
                _G_apply_302, lastError = self._apply(self.rule_ReturnItem, "ReturnItem", [])
                self.considerError(lastError, None)
                return (_G_apply_302, self.currentError)
            _G_or_303, lastError = self._or([_G_or_299, _G_or_301])
            self.considerError(lastError, 'ReturnItems')
            _locals['head'] = _G_or_303
            def _G_many_304():
                self._trace('dy', (2123, 2125), self.input.position)
                _G_apply_305, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace(' = R', (2125, 2129), self.input.position)
                _G_exactly_306, lastError = self.exactly(',')
                self.considerError(lastError, None)
                self._trace('etu', (2129, 2132), self.input.position)
                _G_apply_307, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('rnItems:ri ', (2132, 2143), self.input.position)
                _G_apply_308, lastError = self._apply(self.rule_ReturnItem, "ReturnItem", [])
                self.considerError(lastError, None)
                return (_G_apply_308, self.currentError)
            _G_many_309, lastError = self.many(_G_many_304)
            self.considerError(lastError, 'ReturnItems')
            _locals['tail'] = _G_many_309
            _G_python_311, lastError = eval(self._G_expr_310, self.globals, _locals), None
            self.considerError(lastError, 'ReturnItems')
            return (_G_python_311, self.currentError)


        def rule_ReturnItem(self):
            _locals = {'self': self}
            self.locals['ReturnItem'] = _locals
            def _G_or_312():
                self._trace('", ri, o, s', (2199, 2210), self.input.position)
                _G_apply_313, lastError = self._apply(self.rule_Expression, "Expression", [])
                self.considerError(lastError, None)
                _locals['ex'] = _G_apply_313
                self._trace(']\n\n', (2213, 2216), self.input.position)
                _G_apply_314, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('  ', (2216, 2218), self.input.position)
                _G_apply_315, lastError = self._apply(self.rule_A, "A", [])
                self.considerError(lastError, None)
                self._trace('  ', (2218, 2220), self.input.position)
                _G_apply_316, lastError = self._apply(self.rule_S, "S", [])
                self.considerError(lastError, None)
                self._trace('Ret', (2220, 2223), self.input.position)
                _G_apply_317, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace("urnItems = ('", (2223, 2236), self.input.position)
                _G_apply_318, lastError = self._apply(self.rule_SymbolicName, "SymbolicName", [])
                self.considerError(lastError, None)
                _locals['s'] = _G_apply_318
                _G_python_320, lastError = eval(self._G_expr_319, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_320, self.currentError)
            def _G_or_321():
                self._trace("S ',' WS Re", (2276, 2287), self.input.position)
                _G_apply_322, lastError = self._apply(self.rule_Expression, "Expression", [])
                self.considerError(lastError, None)
                _locals['ex'] = _G_apply_322
                _G_python_324, lastError = eval(self._G_expr_323, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_324, self.currentError)
            _G_or_325, lastError = self._or([_G_or_312, _G_or_321])
            self.considerError(lastError, 'ReturnItem')
            return (_G_or_325, self.currentError)


        def rule_Order(self):
            _locals = {'self': self}
            self.locals['Order'] = _locals
            self._trace('d] ', (2327, 2330), self.input.position)
            _G_apply_326, lastError = self._apply(self.rule_O, "O", [])
            self.considerError(lastError, 'Order')
            self._trace('+ ', (2330, 2332), self.input.position)
            _G_apply_327, lastError = self._apply(self.rule_R, "R", [])
            self.considerError(lastError, 'Order')
            self._trace('ta', (2332, 2334), self.input.position)
            _G_apply_328, lastError = self._apply(self.rule_D, "D", [])
            self.considerError(lastError, 'Order')
            self._trace('il', (2334, 2336), self.input.position)
            _G_apply_329, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'Order')
            self._trace(']\n', (2336, 2338), self.input.position)
            _G_apply_330, lastError = self._apply(self.rule_R, "R", [])
            self.considerError(lastError, 'Order')
            self._trace('\n  ', (2338, 2341), self.input.position)
            _G_apply_331, lastError = self._apply(self.rule_SP, "SP", [])
            self.considerError(lastError, 'Order')
            self._trace('  ', (2341, 2343), self.input.position)
            _G_apply_332, lastError = self._apply(self.rule_B, "B", [])
            self.considerError(lastError, 'Order')
            self._trace('Re', (2343, 2345), self.input.position)
            _G_apply_333, lastError = self._apply(self.rule_Y, "Y", [])
            self.considerError(lastError, 'Order')
            self._trace('tur', (2345, 2348), self.input.position)
            _G_apply_334, lastError = self._apply(self.rule_SP, "SP", [])
            self.considerError(lastError, 'Order')
            self._trace('nItem = E', (2348, 2357), self.input.position)
            _G_apply_335, lastError = self._apply(self.rule_SortItem, "SortItem", [])
            self.considerError(lastError, 'Order')
            _locals['head'] = _G_apply_335
            def _G_many_336():
                self._trace('on:', (2364, 2367), self.input.position)
                _G_exactly_337, lastError = self.exactly(',')
                self.considerError(lastError, None)
                self._trace('ex ', (2367, 2370), self.input.position)
                _G_apply_338, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('SP A S SP', (2370, 2379), self.input.position)
                _G_apply_339, lastError = self._apply(self.rule_SortItem, "SortItem", [])
                self.considerError(lastError, None)
                return (_G_apply_339, self.currentError)
            _G_many_340, lastError = self.many(_G_many_336)
            self.considerError(lastError, 'Order')
            _locals['tail'] = _G_many_340
            _G_python_342, lastError = eval(self._G_expr_341, self.globals, _locals), None
            self.considerError(lastError, 'Order')
            return (_G_python_342, self.currentError)


        def rule_Skip(self):
            _locals = {'self': self}
            self.locals['Skip'] = _locals
            self._trace('   ', (2422, 2425), self.input.position)
            _G_apply_343, lastError = self._apply(self.rule_S, "S", [])
            self.considerError(lastError, 'Skip')
            self._trace('  ', (2425, 2427), self.input.position)
            _G_apply_344, lastError = self._apply(self.rule_K, "K", [])
            self.considerError(lastError, 'Skip')
            self._trace('  ', (2427, 2429), self.input.position)
            _G_apply_345, lastError = self._apply(self.rule_I, "I", [])
            self.considerError(lastError, 'Skip')
            self._trace('  ', (2429, 2431), self.input.position)
            _G_apply_346, lastError = self._apply(self.rule_P, "P", [])
            self.considerError(lastError, 'Skip')
            self._trace('   ', (2431, 2434), self.input.position)
            _G_apply_347, lastError = self._apply(self.rule_SP, "SP", [])
            self.considerError(lastError, 'Skip')
            self._trace(' | Expressi', (2434, 2445), self.input.position)
            _G_apply_348, lastError = self._apply(self.rule_Expression, "Expression", [])
            self.considerError(lastError, 'Skip')
            _locals['ex'] = _G_apply_348
            _G_python_350, lastError = eval(self._G_expr_349, self.globals, _locals), None
            self.considerError(lastError, 'Skip')
            return (_G_python_350, self.currentError)


        def rule_Limit(self):
            _locals = {'self': self}
            self.locals['Limit'] = _locals
            self._trace('Non', (2473, 2476), self.input.position)
            _G_apply_351, lastError = self._apply(self.rule_L, "L", [])
            self.considerError(lastError, 'Limit')
            self._trace('e]', (2476, 2478), self.input.position)
            _G_apply_352, lastError = self._apply(self.rule_I, "I", [])
            self.considerError(lastError, 'Limit')
            self._trace('\n\n', (2478, 2480), self.input.position)
            _G_apply_353, lastError = self._apply(self.rule_M, "M", [])
            self.considerError(lastError, 'Limit')
            self._trace('  ', (2480, 2482), self.input.position)
            _G_apply_354, lastError = self._apply(self.rule_I, "I", [])
            self.considerError(lastError, 'Limit')
            self._trace('  ', (2482, 2484), self.input.position)
            _G_apply_355, lastError = self._apply(self.rule_T, "T", [])
            self.considerError(lastError, 'Limit')
            self._trace('Ord', (2484, 2487), self.input.position)
            _G_apply_356, lastError = self._apply(self.rule_SP, "SP", [])
            self.considerError(lastError, 'Limit')
            self._trace('er =  O R D', (2487, 2498), self.input.position)
            _G_apply_357, lastError = self._apply(self.rule_Expression, "Expression", [])
            self.considerError(lastError, 'Limit')
            _locals['ex'] = _G_apply_357
            _G_python_359, lastError = eval(self._G_expr_358, self.globals, _locals), None
            self.considerError(lastError, 'Limit')
            return (_G_python_359, self.currentError)


        def rule_SortItem(self):
            _locals = {'self': self}
            self.locals['SortItem'] = _locals
            def _G_or_360():
                self._trace("' WS SortIt", (2530, 2541), self.input.position)
                _G_apply_361, lastError = self._apply(self.rule_Expression, "Expression", [])
                self.considerError(lastError, None)
                _locals['ex'] = _G_apply_361
                def _G_or_362():
                    self._trace('ta', (2546, 2548), self.input.position)
                    _G_apply_363, lastError = self._apply(self.rule_SP, "SP", [])
                    self.considerError(lastError, None)
                    self._trace('il', (2548, 2550), self.input.position)
                    _G_apply_364, lastError = self._apply(self.rule_D, "D", [])
                    self.considerError(lastError, None)
                    self._trace(' -', (2550, 2552), self.input.position)
                    _G_apply_365, lastError = self._apply(self.rule_E, "E", [])
                    self.considerError(lastError, None)
                    self._trace('> ', (2552, 2554), self.input.position)
                    _G_apply_366, lastError = self._apply(self.rule_S, "S", [])
                    self.considerError(lastError, None)
                    self._trace('["', (2554, 2556), self.input.position)
                    _G_apply_367, lastError = self._apply(self.rule_C, "C", [])
                    self.considerError(lastError, None)
                    self._trace('Or', (2556, 2558), self.input.position)
                    _G_apply_368, lastError = self._apply(self.rule_E, "E", [])
                    self.considerError(lastError, None)
                    self._trace('de', (2558, 2560), self.input.position)
                    _G_apply_369, lastError = self._apply(self.rule_N, "N", [])
                    self.considerError(lastError, None)
                    self._trace('r"', (2560, 2562), self.input.position)
                    _G_apply_370, lastError = self._apply(self.rule_D, "D", [])
                    self.considerError(lastError, None)
                    self._trace(', ', (2562, 2564), self.input.position)
                    _G_apply_371, lastError = self._apply(self.rule_I, "I", [])
                    self.considerError(lastError, None)
                    self._trace('[h', (2564, 2566), self.input.position)
                    _G_apply_372, lastError = self._apply(self.rule_N, "N", [])
                    self.considerError(lastError, None)
                    self._trace('ea', (2566, 2568), self.input.position)
                    _G_apply_373, lastError = self._apply(self.rule_G, "G", [])
                    self.considerError(lastError, None)
                    return (_G_apply_373, self.currentError)
                def _G_or_374():
                    self._trace(' + ', (2570, 2573), self.input.position)
                    _G_apply_375, lastError = self._apply(self.rule_SP, "SP", [])
                    self.considerError(lastError, None)
                    self._trace('ta', (2573, 2575), self.input.position)
                    _G_apply_376, lastError = self._apply(self.rule_D, "D", [])
                    self.considerError(lastError, None)
                    self._trace('il', (2575, 2577), self.input.position)
                    _G_apply_377, lastError = self._apply(self.rule_E, "E", [])
                    self.considerError(lastError, None)
                    self._trace(']\n', (2577, 2579), self.input.position)
                    _G_apply_378, lastError = self._apply(self.rule_S, "S", [])
                    self.considerError(lastError, None)
                    self._trace('\n ', (2579, 2581), self.input.position)
                    _G_apply_379, lastError = self._apply(self.rule_C, "C", [])
                    self.considerError(lastError, None)
                    return (_G_apply_379, self.currentError)
                _G_or_380, lastError = self._or([_G_or_362, _G_or_374])
                self.considerError(lastError, None)
                _G_python_382, lastError = eval(self._G_expr_381, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_382, self.currentError)
            def _G_or_383():
                self._trace('-> ["Skip",', (2617, 2628), self.input.position)
                _G_apply_384, lastError = self._apply(self.rule_Expression, "Expression", [])
                self.considerError(lastError, None)
                _locals['ex'] = _G_apply_384
                def _G_optional_385():
                    def _G_or_386():
                        self._trace('\n ', (2633, 2635), self.input.position)
                        _G_apply_387, lastError = self._apply(self.rule_SP, "SP", [])
                        self.considerError(lastError, None)
                        self._trace('  ', (2635, 2637), self.input.position)
                        _G_apply_388, lastError = self._apply(self.rule_A, "A", [])
                        self.considerError(lastError, None)
                        self._trace(' L', (2637, 2639), self.input.position)
                        _G_apply_389, lastError = self._apply(self.rule_S, "S", [])
                        self.considerError(lastError, None)
                        self._trace('im', (2639, 2641), self.input.position)
                        _G_apply_390, lastError = self._apply(self.rule_C, "C", [])
                        self.considerError(lastError, None)
                        self._trace('it', (2641, 2643), self.input.position)
                        _G_apply_391, lastError = self._apply(self.rule_E, "E", [])
                        self.considerError(lastError, None)
                        self._trace(' =', (2643, 2645), self.input.position)
                        _G_apply_392, lastError = self._apply(self.rule_N, "N", [])
                        self.considerError(lastError, None)
                        self._trace('  ', (2645, 2647), self.input.position)
                        _G_apply_393, lastError = self._apply(self.rule_D, "D", [])
                        self.considerError(lastError, None)
                        self._trace('L ', (2647, 2649), self.input.position)
                        _G_apply_394, lastError = self._apply(self.rule_I, "I", [])
                        self.considerError(lastError, None)
                        self._trace('I ', (2649, 2651), self.input.position)
                        _G_apply_395, lastError = self._apply(self.rule_N, "N", [])
                        self.considerError(lastError, None)
                        self._trace('M ', (2651, 2653), self.input.position)
                        _G_apply_396, lastError = self._apply(self.rule_G, "G", [])
                        self.considerError(lastError, None)
                        return (_G_apply_396, self.currentError)
                    def _G_or_397():
                        self._trace('T S', (2655, 2658), self.input.position)
                        _G_apply_398, lastError = self._apply(self.rule_SP, "SP", [])
                        self.considerError(lastError, None)
                        self._trace('P ', (2658, 2660), self.input.position)
                        _G_apply_399, lastError = self._apply(self.rule_A, "A", [])
                        self.considerError(lastError, None)
                        self._trace('Ex', (2660, 2662), self.input.position)
                        _G_apply_400, lastError = self._apply(self.rule_S, "S", [])
                        self.considerError(lastError, None)
                        self._trace('pr', (2662, 2664), self.input.position)
                        _G_apply_401, lastError = self._apply(self.rule_C, "C", [])
                        self.considerError(lastError, None)
                        return (_G_apply_401, self.currentError)
                    _G_or_402, lastError = self._or([_G_or_386, _G_or_397])
                    self.considerError(lastError, None)
                    return (_G_or_402, self.currentError)
                def _G_optional_403():
                    return (None, self.input.nullError())
                _G_or_404, lastError = self._or([_G_optional_385, _G_optional_403])
                self.considerError(lastError, None)
                _G_python_406, lastError = eval(self._G_expr_405, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_406, self.currentError)
            _G_or_407, lastError = self._or([_G_or_360, _G_or_383])
            self.considerError(lastError, 'SortItem')
            return (_G_or_407, self.currentError)


        def rule_Where(self):
            _locals = {'self': self}
            self.locals['Where'] = _locals
            self._trace('rt', (2698, 2700), self.input.position)
            _G_apply_408, lastError = self._apply(self.rule_W, "W", [])
            self.considerError(lastError, 'Where')
            self._trace('It', (2700, 2702), self.input.position)
            _G_apply_409, lastError = self._apply(self.rule_H, "H", [])
            self.considerError(lastError, 'Where')
            self._trace('em', (2702, 2704), self.input.position)
            _G_apply_410, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'Where')
            self._trace(' =', (2704, 2706), self.input.position)
            _G_apply_411, lastError = self._apply(self.rule_R, "R", [])
            self.considerError(lastError, 'Where')
            self._trace(' E', (2706, 2708), self.input.position)
            _G_apply_412, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'Where')
            self._trace('xpr', (2708, 2711), self.input.position)
            _G_apply_413, lastError = self._apply(self.rule_SP, "SP", [])
            self.considerError(lastError, 'Where')
            self._trace('ession:ex (', (2711, 2722), self.input.position)
            _G_apply_414, lastError = self._apply(self.rule_Expression, "Expression", [])
            self.considerError(lastError, 'Where')
            _locals['ex'] = _G_apply_414
            _G_python_416, lastError = eval(self._G_expr_415, self.globals, _locals), None
            self.considerError(lastError, 'Where')
            return (_G_python_416, self.currentError)


        def rule_Pattern(self):
            _locals = {'self': self}
            self.locals['Pattern'] = _locals
            self._trace(' S C) -> ["s', (2753, 2765), self.input.position)
            _G_apply_417, lastError = self._apply(self.rule_PatternPart, "PatternPart", [])
            self.considerError(lastError, 'Pattern')
            _locals['head'] = _G_apply_417
            def _G_many_418():
                self._trace('x, ', (2772, 2775), self.input.position)
                _G_exactly_419, lastError = self.exactly(',')
                self.considerError(lastError, None)
                self._trace('"de', (2775, 2778), self.input.position)
                _G_apply_420, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('sc"]\n       ', (2778, 2790), self.input.position)
                _G_apply_421, lastError = self._apply(self.rule_PatternPart, "PatternPart", [])
                self.considerError(lastError, None)
                return (_G_apply_421, self.currentError)
            _G_many_422, lastError = self.many(_G_many_418)
            self.considerError(lastError, 'Pattern')
            _locals['tail'] = _G_many_422
            _G_python_424, lastError = eval(self._G_expr_423, self.globals, _locals), None
            self.considerError(lastError, 'Pattern')
            return (_G_python_424, self.currentError)


        def rule_PatternPart(self):
            _locals = {'self': self}
            self.locals['PatternPart'] = _locals
            def _G_or_425():
                self._trace(' G | SP ', (2831, 2839), self.input.position)
                _G_apply_426, lastError = self._apply(self.rule_Variable, "Variable", [])
                self.considerError(lastError, None)
                _locals['v'] = _G_apply_426
                self._trace('S C', (2841, 2844), self.input.position)
                _G_apply_427, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace(')? -', (2844, 2848), self.input.position)
                _G_exactly_428, lastError = self.exactly('=')
                self.considerError(lastError, None)
                self._trace('> [', (2848, 2851), self.input.position)
                _G_apply_429, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('"sort", ex, "asc"]\n\n ', (2851, 2872), self.input.position)
                _G_apply_430, lastError = self._apply(self.rule_AnonymousPatternPart, "AnonymousPatternPart", [])
                self.considerError(lastError, None)
                _locals['ap'] = _G_apply_430
                _G_python_432, lastError = eval(self._G_expr_431, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_432, self.currentError)
            def _G_or_433():
                self._trace('re", ex]', (2918, 2926), self.input.position)
                _G_apply_434, lastError = self._apply(self.rule_Variable, "Variable", [])
                self.considerError(lastError, None)
                _locals['v'] = _G_apply_434
                self._trace('    ', (2928, 2932), self.input.position)
                _G_exactly_435, lastError = self.exactly(':')
                self.considerError(lastError, None)
                self._trace('Pat', (2932, 2935), self.input.position)
                _G_apply_436, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('tern = PatternPart:he', (2935, 2956), self.input.position)
                _G_apply_437, lastError = self._apply(self.rule_AnonymousPatternPart, "AnonymousPatternPart", [])
                self.considerError(lastError, None)
                _locals['ap'] = _G_apply_437
                _G_python_439, lastError = eval(self._G_expr_438, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_439, self.currentError)
            def _G_or_440():
                self._trace('   PatternPart = (Var', (3005, 3026), self.input.position)
                _G_apply_441, lastError = self._apply(self.rule_AnonymousPatternPart, "AnonymousPatternPart", [])
                self.considerError(lastError, None)
                _locals['ap'] = _G_apply_441
                _G_python_443, lastError = eval(self._G_expr_442, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_443, self.currentError)
            _G_or_444, lastError = self._or([_G_or_425, _G_or_433, _G_or_440])
            self.considerError(lastError, 'PatternPart')
            return (_G_or_444, self.currentError)


        def rule_AnonymousPatternPart(self):
            _locals = {'self': self}
            self.locals['AnonymousPatternPart'] = _locals
            self._trace('art", v, ap]\n  ', (3082, 3097), self.input.position)
            _G_apply_445, lastError = self._apply(self.rule_PatternElement, "PatternElement", [])
            self.considerError(lastError, 'AnonymousPatternPart')
            return (_G_apply_445, self.currentError)


        def rule_PatternElement(self):
            _locals = {'self': self}
            self.locals['PatternElement'] = _locals
            def _G_or_446():
                self._trace("iable:v ':' WS AnonymousPatternP", (3117, 3149), self.input.position)
                _G_apply_447, lastError = self._apply(self.rule_NodePattern, "NodePattern", [])
                self.considerError(lastError, None)
                _locals['np'] = _G_apply_447
                def _G_many_448():
                    self._trace('Pa', (3174, 3176), self.input.position)
                    _G_apply_449, lastError = self._apply(self.rule_WS, "WS", [])
                    self.considerError(lastError, None)
                    self._trace('rt", v, ap]\n        ', (3176, 3196), self.input.position)
                    _G_apply_450, lastError = self._apply(self.rule_PatternElementChain, "PatternElementChain", [])
                    self.considerError(lastError, None)
                    return (_G_apply_450, self.currentError)
                _G_many_451, lastError = self.many(_G_many_448)
                self.considerError(lastError, None)
                _locals['pec'] = _G_many_451
                _G_python_453, lastError = eval(self._G_expr_452, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_453, self.currentError)
            def _G_or_454():
                self._trace('mous', (3269, 3273), self.input.position)
                _G_exactly_455, lastError = self.exactly('(')
                self.considerError(lastError, None)
                self._trace('PatternPart = P', (3273, 3288), self.input.position)
                _G_apply_456, lastError = self._apply(self.rule_PatternElement, "PatternElement", [])
                self.considerError(lastError, None)
                _locals['pe'] = _G_apply_456
                self._trace('ernE', (3291, 3295), self.input.position)
                _G_exactly_457, lastError = self.exactly(')')
                self.considerError(lastError, None)
                _G_python_459, lastError = eval(self._G_expr_458, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_459, self.currentError)
            _G_or_460, lastError = self._or([_G_or_446, _G_or_454])
            self.considerError(lastError, 'PatternElement')
            return (_G_or_460, self.currentError)


        def rule_NodePattern(self):
            _locals = {'self': self}
            self.locals['NodePattern'] = _locals
            self._trace('emen', (3316, 3320), self.input.position)
            _G_exactly_461, lastError = self.exactly('(')
            self.considerError(lastError, 'NodePattern')
            self._trace('t =', (3320, 3323), self.input.position)
            _G_apply_462, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'NodePattern')
            def _G_optional_463():
                self._trace('            NodePattern:np\n  ', (3338, 3367), self.input.position)
                _G_apply_464, lastError = self._apply(self.rule_SymbolicName, "SymbolicName", [])
                self.considerError(lastError, None)
                _locals['s'] = _G_apply_464
                self._trace('   ', (3369, 3372), self.input.position)
                _G_apply_465, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                _G_python_466, lastError = eval(self._G_expr_9, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_466, self.currentError)
            def _G_optional_467():
                return (None, self.input.nullError())
            _G_or_468, lastError = self._or([_G_optional_463, _G_optional_467])
            self.considerError(lastError, 'NodePattern')
            _locals['s'] = _G_or_468
            def _G_optional_469():
                self._trace('in)*:pec\n                   ', (3410, 3438), self.input.position)
                _G_apply_470, lastError = self._apply(self.rule_NodeLabels, "NodeLabels", [])
                self.considerError(lastError, None)
                _locals['nl'] = _G_apply_470
                self._trace('-> ', (3441, 3444), self.input.position)
                _G_apply_471, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                _G_python_473, lastError = eval(self._G_expr_472, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_473, self.currentError)
            def _G_optional_474():
                return (None, self.input.nullError())
            _G_or_475, lastError = self._or([_G_optional_469, _G_optional_474])
            self.considerError(lastError, 'NodePattern')
            _locals['nl'] = _G_or_475
            def _G_optional_476():
                self._trace("        | '(' PatternElement", (3484, 3512), self.input.position)
                _G_apply_477, lastError = self._apply(self.rule_Properties, "Properties", [])
                self.considerError(lastError, None)
                _locals['p'] = _G_apply_477
                self._trace("e '", (3514, 3517), self.input.position)
                _G_apply_478, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                _G_python_480, lastError = eval(self._G_expr_479, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_480, self.currentError)
            def _G_optional_481():
                return (None, self.input.nullError())
            _G_or_482, lastError = self._or([_G_optional_476, _G_optional_481])
            self.considerError(lastError, 'NodePattern')
            _locals['p'] = _G_or_482
            self._trace("rn = '(' WS\n    ", (3540, 3556), self.input.position)
            _G_exactly_483, lastError = self.exactly(')')
            self.considerError(lastError, 'NodePattern')
            _G_python_485, lastError = eval(self._G_expr_484, self.globals, _locals), None
            self.considerError(lastError, 'NodePattern')
            return (_G_python_485, self.currentError)


        def rule_PatternElementChain(self):
            _locals = {'self': self}
            self.locals['PatternElementChain'] = _locals
            self._trace(' -> s\n              ', (3608, 3628), self.input.position)
            _G_apply_486, lastError = self._apply(self.rule_RelationshipPattern, "RelationshipPattern", [])
            self.considerError(lastError, 'PatternElementChain')
            _locals['rp'] = _G_apply_486
            self._trace(')?:', (3631, 3634), self.input.position)
            _G_apply_487, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'PatternElementChain')
            self._trace('s\n          ', (3634, 3646), self.input.position)
            _G_apply_488, lastError = self._apply(self.rule_NodePattern, "NodePattern", [])
            self.considerError(lastError, 'PatternElementChain')
            _locals['np'] = _G_apply_488
            _G_python_490, lastError = eval(self._G_expr_489, self.globals, _locals), None
            self.considerError(lastError, 'PatternElementChain')
            return (_G_python_490, self.currentError)


        def rule_RelationshipPattern(self):
            _locals = {'self': self}
            self.locals['RelationshipPattern'] = _locals
            def _G_optional_491():
                self._trace('         )?:nl', (3707, 3721), self.input.position)
                _G_apply_492, lastError = self._apply(self.rule_LeftArrowHead, "LeftArrowHead", [])
                self.considerError(lastError, None)
                return (_G_apply_492, self.currentError)
            def _G_optional_493():
                return (None, self.input.nullError())
            _G_or_494, lastError = self._or([_G_optional_491, _G_optional_493])
            self.considerError(lastError, 'RelationshipPattern')
            _locals['la'] = _G_or_494
            self._trace('   ', (3725, 3728), self.input.position)
            _G_apply_495, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'RelationshipPattern')
            self._trace('     ', (3728, 3733), self.input.position)
            _G_apply_496, lastError = self._apply(self.rule_Dash, "Dash", [])
            self.considerError(lastError, 'RelationshipPattern')
            self._trace('   ', (3733, 3736), self.input.position)
            _G_apply_497, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'RelationshipPattern')
            def _G_optional_498():
                self._trace('   (\n              ', (3736, 3755), self.input.position)
                _G_apply_499, lastError = self._apply(self.rule_RelationshipDetail, "RelationshipDetail", [])
                self.considerError(lastError, None)
                return (_G_apply_499, self.currentError)
            def _G_optional_500():
                return (None, self.input.nullError())
            _G_or_501, lastError = self._or([_G_optional_498, _G_optional_500])
            self.considerError(lastError, 'RelationshipPattern')
            _locals['rd'] = _G_or_501
            self._trace('   ', (3759, 3762), self.input.position)
            _G_apply_502, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'RelationshipPattern')
            self._trace('Prope', (3762, 3767), self.input.position)
            _G_apply_503, lastError = self._apply(self.rule_Dash, "Dash", [])
            self.considerError(lastError, 'RelationshipPattern')
            self._trace('rti', (3767, 3770), self.input.position)
            _G_apply_504, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'RelationshipPattern')
            def _G_optional_505():
                self._trace('es:p WS -> p\n  ', (3770, 3785), self.input.position)
                _G_apply_506, lastError = self._apply(self.rule_RightArrowHead, "RightArrowHead", [])
                self.considerError(lastError, None)
                return (_G_apply_506, self.currentError)
            def _G_optional_507():
                return (None, self.input.nullError())
            _G_or_508, lastError = self._or([_G_optional_505, _G_optional_507])
            self.considerError(lastError, 'RelationshipPattern')
            _locals['ra'] = _G_or_508
            _G_python_510, lastError = eval(self._G_expr_509, self.globals, _locals), None
            self.considerError(lastError, 'RelationshipPattern')
            return (_G_python_510, self.currentError)


        def rule_RelationshipDetail(self):
            _locals = {'self': self}
            self.locals['RelationshipDetail'] = _locals
            self._trace('entC', (3938, 3942), self.input.position)
            _G_exactly_511, lastError = self.exactly('[')
            self.considerError(lastError, 'RelationshipDetail')
            def _G_optional_512():
                self._trace('hain", rp, np]\n\n    Relatio', (3942, 3969), self.input.position)
                _G_apply_513, lastError = self._apply(self.rule_Variable, "Variable", [])
                self.considerError(lastError, None)
                return (_G_apply_513, self.currentError)
            def _G_optional_514():
                return (None, self.input.nullError())
            _G_or_515, lastError = self._or([_G_optional_512, _G_optional_514])
            self.considerError(lastError, 'RelationshipDetail')
            _locals['v'] = _G_or_515
            def _G_optional_516():
                self._trace('ipPattern = LeftArrowH', (3972, 3994), self.input.position)
                _G_exactly_517, lastError = self.exactly('?')
                self.considerError(lastError, None)
                return (_G_exactly_517, self.currentError)
            def _G_optional_518():
                return (None, self.input.nullError())
            _G_or_519, lastError = self._or([_G_optional_516, _G_optional_518])
            self.considerError(lastError, 'RelationshipDetail')
            _locals['q'] = _G_or_519
            def _G_optional_520():
                self._trace('?:la WS Dash WS RelationshipDetail?:', (3997, 4033), self.input.position)
                _G_apply_521, lastError = self._apply(self.rule_RelationshipTypes, "RelationshipTypes", [])
                self.considerError(lastError, None)
                return (_G_apply_521, self.currentError)
            def _G_optional_522():
                return (None, self.input.nullError())
            _G_or_523, lastError = self._or([_G_optional_520, _G_optional_522])
            self.considerError(lastError, 'RelationshipDetail')
            _locals['rt'] = _G_or_523
            def _G_optional_524():
                self._trace('Hea', (4057, 4060), self.input.position)
                _G_exactly_525, lastError = self.exactly('*')
                self.considerError(lastError, None)
                self._trace('d?:ra -> ["Re', (4060, 4073), self.input.position)
                _G_apply_526, lastError = self._apply(self.rule_RangeLiteral, "RangeLiteral", [])
                self.considerError(lastError, None)
                return (_G_apply_526, self.currentError)
            def _G_optional_527():
                return (None, self.input.nullError())
            _G_or_528, lastError = self._or([_G_optional_524, _G_optional_527])
            self.considerError(lastError, 'RelationshipDetail')
            _locals['rl'] = _G_or_528
            self._trace('nsh', (4078, 4081), self.input.position)
            _G_apply_529, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'RelationshipDetail')
            def _G_optional_530():
                self._trace('ipsPattern", la, rd, ra]\n\n   ', (4081, 4110), self.input.position)
                _G_apply_531, lastError = self._apply(self.rule_Properties, "Properties", [])
                self.considerError(lastError, None)
                return (_G_apply_531, self.currentError)
            def _G_optional_532():
                return (None, self.input.nullError())
            _G_or_533, lastError = self._or([_G_optional_530, _G_optional_532])
            self.considerError(lastError, 'RelationshipDetail')
            _locals['p'] = _G_or_533
            self._trace('TO DO: fix WS handling', (4113, 4135), self.input.position)
            _G_exactly_534, lastError = self.exactly(']')
            self.considerError(lastError, 'RelationshipDetail')
            _G_python_536, lastError = eval(self._G_expr_535, self.globals, _locals), None
            self.considerError(lastError, 'RelationshipDetail')
            return (_G_python_536, self.currentError)


        def rule_Properties(self):
            _locals = {'self': self}
            self.locals['Properties'] = _locals
            def _G_or_537():
                self._trace('tern:\n    R', (4192, 4203), self.input.position)
                _G_apply_538, lastError = self._apply(self.rule_MapLiteral, "MapLiteral", [])
                self.considerError(lastError, None)
                return (_G_apply_538, self.currentError)
            def _G_or_539():
                self._trace("tail = '['", (4216, 4226), self.input.position)
                _G_apply_540, lastError = self._apply(self.rule_Parameter, "Parameter", [])
                self.considerError(lastError, None)
                return (_G_apply_540, self.currentError)
            _G_or_541, lastError = self._or([_G_or_537, _G_or_539])
            self.considerError(lastError, 'Properties')
            return (_G_or_541, self.currentError)


        def rule_RelationshipTypes(self):
            _locals = {'self': self}
            self.locals['RelationshipTypes'] = _locals
            self._trace('  Va', (4247, 4251), self.input.position)
            _G_exactly_542, lastError = self.exactly(':')
            self.considerError(lastError, 'RelationshipTypes')
            self._trace('riable?:v\n  ', (4251, 4263), self.input.position)
            _G_apply_543, lastError = self._apply(self.rule_RelTypeName, "RelTypeName", [])
            self.considerError(lastError, 'RelationshipTypes')
            _locals['head'] = _G_apply_543
            def _G_many_544():
                self._trace('  ', (4270, 4272), self.input.position)
                _G_apply_545, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('    ', (4272, 4276), self.input.position)
                _G_exactly_546, lastError = self.exactly('|')
                self.considerError(lastError, None)
                def _G_optional_547():
                    self._trace('    ', (4276, 4280), self.input.position)
                    _G_exactly_548, lastError = self.exactly(':')
                    self.considerError(lastError, None)
                    return (_G_exactly_548, self.currentError)
                def _G_optional_549():
                    return (None, self.input.nullError())
                _G_or_550, lastError = self._or([_G_optional_547, _G_optional_549])
                self.considerError(lastError, None)
                self._trace("  '", (4281, 4284), self.input.position)
                _G_apply_551, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace("?'?:q\n      ", (4284, 4296), self.input.position)
                _G_apply_552, lastError = self._apply(self.rule_RelTypeName, "RelTypeName", [])
                self.considerError(lastError, None)
                return (_G_apply_552, self.currentError)
            _G_many_553, lastError = self.many(_G_many_544)
            self.considerError(lastError, 'RelationshipTypes')
            _locals['tail'] = _G_many_553
            _G_python_555, lastError = eval(self._G_expr_554, self.globals, _locals), None
            self.considerError(lastError, 'RelationshipTypes')
            return (_G_python_555, self.currentError)


        def rule_NodeLabels(self):
            _locals = {'self': self}
            self.locals['NodeLabels'] = _locals
            self._trace(" ('*' Rang", (4355, 4365), self.input.position)
            _G_apply_556, lastError = self._apply(self.rule_NodeLabel, "NodeLabel", [])
            self.considerError(lastError, 'NodeLabels')
            _locals['head'] = _G_apply_556
            def _G_many_557():
                self._trace('l)', (4372, 4374), self.input.position)
                _G_apply_558, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('?:rl WS\n  ', (4374, 4384), self.input.position)
                _G_apply_559, lastError = self._apply(self.rule_NodeLabel, "NodeLabel", [])
                self.considerError(lastError, None)
                return (_G_apply_559, self.currentError)
            _G_many_560, lastError = self.many(_G_many_557)
            self.considerError(lastError, 'NodeLabels')
            _locals['tail'] = _G_many_560
            _G_python_561, lastError = eval(self._G_expr_423, self.globals, _locals), None
            self.considerError(lastError, 'NodeLabels')
            return (_G_python_561, self.currentError)


        def rule_NodeLabel(self):
            _locals = {'self': self}
            self.locals['NodeLabel'] = _locals
            self._trace('    ', (4421, 4425), self.input.position)
            _G_exactly_562, lastError = self.exactly(':')
            self.considerError(lastError, 'NodeLabel')
            self._trace('          ', (4425, 4435), self.input.position)
            _G_apply_563, lastError = self._apply(self.rule_LabelName, "LabelName", [])
            self.considerError(lastError, 'NodeLabel')
            _locals['n'] = _G_apply_563
            _G_python_565, lastError = eval(self._G_expr_564, self.globals, _locals), None
            self.considerError(lastError, 'NodeLabel')
            return (_G_python_565, self.currentError)


        def rule_RangeLiteral(self):
            _locals = {'self': self}
            self.locals['RangeLiteral'] = _locals
            def _G_optional_566():
                self._trace(' r', (4475, 4477), self.input.position)
                _G_apply_567, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('t, rl, p]\n\n    ', (4477, 4492), self.input.position)
                _G_apply_568, lastError = self._apply(self.rule_IntegerLiteral, "IntegerLiteral", [])
                self.considerError(lastError, None)
                return (_G_apply_568, self.currentError)
            def _G_optional_569():
                return (None, self.input.nullError())
            _G_or_570, lastError = self._or([_G_optional_566, _G_optional_569])
            self.considerError(lastError, 'RangeLiteral')
            _locals['start'] = _G_or_570
            self._trace('es ', (4500, 4503), self.input.position)
            _G_apply_571, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'RangeLiteral')
            def _G_optional_572():
                self._trace('MapL', (4505, 4509), self.input.position)
                _G_exactly_573, lastError = self.exactly('..')
                self.considerError(lastError, None)
                self._trace('ite', (4509, 4512), self.input.position)
                _G_apply_574, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('ral\n           ', (4512, 4527), self.input.position)
                _G_apply_575, lastError = self._apply(self.rule_IntegerLiteral, "IntegerLiteral", [])
                self.considerError(lastError, None)
                return (_G_apply_575, self.currentError)
            def _G_optional_576():
                return (None, self.input.nullError())
            _G_or_577, lastError = self._or([_G_optional_572, _G_optional_576])
            self.considerError(lastError, 'RangeLiteral')
            _locals['stop'] = _G_or_577
            self._trace('ara', (4534, 4537), self.input.position)
            _G_apply_578, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'RangeLiteral')
            _G_python_580, lastError = eval(self._G_expr_579, self.globals, _locals), None
            self.considerError(lastError, 'RangeLiteral')
            return (_G_python_580, self.currentError)


        def rule_LabelName(self):
            _locals = {'self': self}
            self.locals['LabelName'] = _locals
            self._trace('RelTypeName:h', (4572, 4585), self.input.position)
            _G_apply_581, lastError = self._apply(self.rule_SymbolicName, "SymbolicName", [])
            self.considerError(lastError, 'LabelName')
            return (_G_apply_581, self.currentError)


        def rule_RelTypeName(self):
            _locals = {'self': self}
            self.locals['RelTypeName'] = _locals
            self._trace('? WS RelTypeN', (4600, 4613), self.input.position)
            _G_apply_582, lastError = self._apply(self.rule_SymbolicName, "SymbolicName", [])
            self.considerError(lastError, 'RelTypeName')
            return (_G_apply_582, self.currentError)


        def rule_Expression(self):
            _locals = {'self': self}
            self.locals['Expression'] = _locals
            self._trace('["Relationshi', (4627, 4640), self.input.position)
            _G_apply_583, lastError = self._apply(self.rule_Expression12, "Expression12", [])
            self.considerError(lastError, 'Expression')
            return (_G_apply_583, self.currentError)


        def rule_Expression12(self):
            _locals = {'self': self}
            self.locals['Expression12'] = _locals
            def _G_or_584():
                self._trace(' tail\n\n    No', (4656, 4669), self.input.position)
                _G_apply_585, lastError = self._apply(self.rule_Expression11, "Expression11", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_585
                self._trace('bel', (4673, 4676), self.input.position)
                _G_apply_586, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('s ', (4676, 4678), self.input.position)
                _G_apply_587, lastError = self._apply(self.rule_O, "O", [])
                self.considerError(lastError, None)
                self._trace('= ', (4678, 4680), self.input.position)
                _G_apply_588, lastError = self._apply(self.rule_R, "R", [])
                self.considerError(lastError, None)
                self._trace('Nod', (4680, 4683), self.input.position)
                _G_apply_589, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('eLabel:head (', (4683, 4696), self.input.position)
                _G_apply_590, lastError = self._apply(self.rule_Expression12, "Expression12", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_590
                _G_python_592, lastError = eval(self._G_expr_591, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_592, self.currentError)
            def _G_or_593():
                self._trace('   NodeLabel ', (4735, 4748), self.input.position)
                _G_apply_594, lastError = self._apply(self.rule_Expression11, "Expression11", [])
                self.considerError(lastError, None)
                return (_G_apply_594, self.currentError)
            _G_or_595, lastError = self._or([_G_or_584, _G_or_593])
            self.considerError(lastError, 'Expression12')
            return (_G_or_595, self.currentError)


        def rule_Expression11(self):
            _locals = {'self': self}
            self.locals['Expression11'] = _locals
            def _G_or_596():
                self._trace('n -> ["NodeLa', (4764, 4777), self.input.position)
                _G_apply_597, lastError = self._apply(self.rule_Expression10, "Expression10", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_597
                self._trace(', n', (4781, 4784), self.input.position)
                _G_apply_598, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace(']\n', (4784, 4786), self.input.position)
                _G_apply_599, lastError = self._apply(self.rule_X, "X", [])
                self.considerError(lastError, None)
                self._trace('\n ', (4786, 4788), self.input.position)
                _G_apply_600, lastError = self._apply(self.rule_O, "O", [])
                self.considerError(lastError, None)
                self._trace('  ', (4788, 4790), self.input.position)
                _G_apply_601, lastError = self._apply(self.rule_R, "R", [])
                self.considerError(lastError, None)
                self._trace(' Ra', (4790, 4793), self.input.position)
                _G_apply_602, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('ngeLiteral = ', (4793, 4806), self.input.position)
                _G_apply_603, lastError = self._apply(self.rule_Expression11, "Expression11", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_603
                _G_python_605, lastError = eval(self._G_expr_604, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_605, self.currentError)
            def _G_or_606():
                self._trace('ntegerLiteral', (4846, 4859), self.input.position)
                _G_apply_607, lastError = self._apply(self.rule_Expression10, "Expression10", [])
                self.considerError(lastError, None)
                return (_G_apply_607, self.currentError)
            _G_or_608, lastError = self._or([_G_or_596, _G_or_606])
            self.considerError(lastError, 'Expression11')
            return (_G_or_608, self.currentError)


        def rule_Expression10(self):
            _locals = {'self': self}
            self.locals['Expression10'] = _locals
            def _G_or_609():
                self._trace('ice(start, s', (4875, 4887), self.input.position)
                _G_apply_610, lastError = self._apply(self.rule_Expression9, "Expression9", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_610
                self._trace('\n\n ', (4891, 4894), self.input.position)
                _G_apply_611, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('  ', (4894, 4896), self.input.position)
                _G_apply_612, lastError = self._apply(self.rule_A, "A", [])
                self.considerError(lastError, None)
                self._trace(' L', (4896, 4898), self.input.position)
                _G_apply_613, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace('ab', (4898, 4900), self.input.position)
                _G_apply_614, lastError = self._apply(self.rule_D, "D", [])
                self.considerError(lastError, None)
                self._trace('elN', (4900, 4903), self.input.position)
                _G_apply_615, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('ame = Symboli', (4903, 4916), self.input.position)
                _G_apply_616, lastError = self._apply(self.rule_Expression10, "Expression10", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_616
                _G_python_618, lastError = eval(self._G_expr_617, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_618, self.currentError)
            def _G_or_619():
                self._trace('   Expressio', (4956, 4968), self.input.position)
                _G_apply_620, lastError = self._apply(self.rule_Expression9, "Expression9", [])
                self.considerError(lastError, None)
                return (_G_apply_620, self.currentError)
            _G_or_621, lastError = self._or([_G_or_609, _G_or_619])
            self.considerError(lastError, 'Expression10')
            return (_G_or_621, self.currentError)


        def rule_Expression9(self):
            _locals = {'self': self}
            self.locals['Expression9'] = _locals
            def _G_or_622():
                self._trace('2\n', (4983, 4985), self.input.position)
                _G_apply_623, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace('\n ', (4985, 4987), self.input.position)
                _G_apply_624, lastError = self._apply(self.rule_O, "O", [])
                self.considerError(lastError, None)
                self._trace('  ', (4987, 4989), self.input.position)
                _G_apply_625, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                self._trace(' Ex', (4989, 4992), self.input.position)
                _G_apply_626, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('pression12 =', (4992, 5004), self.input.position)
                _G_apply_627, lastError = self._apply(self.rule_Expression9, "Expression9", [])
                self.considerError(lastError, None)
                _locals['ex'] = _G_apply_627
                _G_python_629, lastError = eval(self._G_expr_628, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_629, self.currentError)
            def _G_or_630():
                self._trace('ession12:ex2', (5036, 5048), self.input.position)
                _G_apply_631, lastError = self._apply(self.rule_Expression8, "Expression8", [])
                self.considerError(lastError, None)
                return (_G_apply_631, self.currentError)
            _G_or_632, lastError = self._or([_G_or_622, _G_or_630])
            self.considerError(lastError, 'Expression9')
            return (_G_or_632, self.currentError)


        def rule_Expression8(self):
            _locals = {'self': self}
            self.locals['Expression8'] = _locals
            def _G_or_633():
                self._trace(' ex2]\n      ', (5063, 5075), self.input.position)
                _G_apply_634, lastError = self._apply(self.rule_Expression7, "Expression7", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_634
                self._trace('   ', (5079, 5082), self.input.position)
                _G_apply_635, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('    ', (5082, 5086), self.input.position)
                _G_exactly_636, lastError = self.exactly('=')
                self.considerError(lastError, None)
                self._trace('| Ex', (5086, 5090), self.input.position)
                _G_apply_637, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('pression11\n\n', (5090, 5102), self.input.position)
                _G_apply_638, lastError = self._apply(self.rule_Expression8, "Expression8", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_638
                _G_python_640, lastError = eval(self._G_expr_639, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_640, self.currentError)
            def _G_or_641():
                self._trace('X O R SP Exp', (5141, 5153), self.input.position)
                _G_apply_642, lastError = self._apply(self.rule_Expression7, "Expression7", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_642
                self._trace('ion', (5157, 5160), self.input.position)
                _G_apply_643, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('11:ex', (5160, 5165), self.input.position)
                _G_exactly_644, lastError = self.exactly('<>')
                self.considerError(lastError, None)
                self._trace('2 -', (5165, 5168), self.input.position)
                _G_apply_645, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('> ["xor", ex', (5168, 5180), self.input.position)
                _G_apply_646, lastError = self._apply(self.rule_Expression8, "Expression8", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_646
                _G_python_648, lastError = eval(self._G_expr_647, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_648, self.currentError)
            def _G_or_649():
                self._trace('\n\n    Expres', (5219, 5231), self.input.position)
                _G_apply_650, lastError = self._apply(self.rule_Expression7, "Expression7", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_650
                self._trace('10 ', (5235, 5238), self.input.position)
                _G_apply_651, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('= Exp', (5238, 5243), self.input.position)
                _G_exactly_652, lastError = self.exactly('!=')
                self.considerError(lastError, None)
                self._trace('res', (5243, 5246), self.input.position)
                _G_apply_653, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('sion9:ex1 SP', (5246, 5258), self.input.position)
                _G_apply_654, lastError = self._apply(self.rule_Expression8, "Expression8", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_654
                _G_python_655, lastError = eval(self._G_expr_647, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_655, self.currentError)
            def _G_or_656():
                self._trace('x1, ex2]\n   ', (5297, 5309), self.input.position)
                _G_apply_657, lastError = self._apply(self.rule_Expression7, "Expression7", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_657
                self._trace('   ', (5313, 5316), self.input.position)
                _G_apply_658, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('    ', (5316, 5320), self.input.position)
                _G_exactly_659, lastError = self.exactly('<')
                self.considerError(lastError, None)
                self._trace('   |', (5320, 5324), self.input.position)
                _G_apply_660, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace(' Expression9', (5324, 5336), self.input.position)
                _G_apply_661, lastError = self._apply(self.rule_Expression8, "Expression8", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_661
                _G_python_663, lastError = eval(self._G_expr_662, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_663, self.currentError)
            def _G_or_664():
                self._trace('9:ex -> ["no', (5375, 5387), self.input.position)
                _G_apply_665, lastError = self._apply(self.rule_Expression7, "Expression7", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_665
                self._trace('ex]', (5391, 5394), self.input.position)
                _G_apply_666, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('\n   ', (5394, 5398), self.input.position)
                _G_exactly_667, lastError = self.exactly('>')
                self.considerError(lastError, None)
                self._trace('    ', (5398, 5402), self.input.position)
                _G_apply_668, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('         | E', (5402, 5414), self.input.position)
                _G_apply_669, lastError = self._apply(self.rule_Expression8, "Expression8", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_669
                _G_python_671, lastError = eval(self._G_expr_670, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_671, self.currentError)
            def _G_or_672():
                self._trace("n7:ex1 WS '=", (5453, 5465), self.input.position)
                _G_apply_673, lastError = self._apply(self.rule_Expression7, "Expression7", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_673
                self._trace('S E', (5469, 5472), self.input.position)
                _G_apply_674, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('xpres', (5472, 5477), self.input.position)
                _G_exactly_675, lastError = self.exactly('<=')
                self.considerError(lastError, None)
                self._trace('sio', (5477, 5480), self.input.position)
                _G_apply_676, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('n8:ex2 -> ["', (5480, 5492), self.input.position)
                _G_apply_677, lastError = self._apply(self.rule_Expression8, "Expression8", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_677
                _G_python_679, lastError = eval(self._G_expr_678, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_679, self.currentError)
            def _G_or_680():
                self._trace('ssion7:ex1 W', (5531, 5543), self.input.position)
                _G_apply_681, lastError = self._apply(self.rule_Expression7, "Expression7", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_681
                self._trace(">' ", (5547, 5550), self.input.position)
                _G_apply_682, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('WS Ex', (5550, 5555), self.input.position)
                _G_exactly_683, lastError = self.exactly('>=')
                self.considerError(lastError, None)
                self._trace('pre', (5555, 5558), self.input.position)
                _G_apply_684, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('ssion8:ex2 -', (5558, 5570), self.input.position)
                _G_apply_685, lastError = self._apply(self.rule_Expression8, "Expression8", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_685
                _G_python_687, lastError = eval(self._G_expr_686, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_687, self.currentError)
            def _G_or_688():
                self._trace('xpression7:e', (5609, 5621), self.input.position)
                _G_apply_689, lastError = self._apply(self.rule_Expression7, "Expression7", [])
                self.considerError(lastError, None)
                return (_G_apply_689, self.currentError)
            _G_or_690, lastError = self._or([_G_or_633, _G_or_641, _G_or_649, _G_or_656, _G_or_664, _G_or_672, _G_or_680, _G_or_688])
            self.considerError(lastError, 'Expression8')
            return (_G_or_690, self.currentError)


        def rule_Expression7(self):
            _locals = {'self': self}
            self.locals['Expression7'] = _locals
            def _G_or_691():
                self._trace('xpression8:e', (5636, 5648), self.input.position)
                _G_apply_692, lastError = self._apply(self.rule_Expression6, "Expression6", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_692
                self._trace('> [', (5652, 5655), self.input.position)
                _G_apply_693, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('"neq', (5655, 5659), self.input.position)
                _G_exactly_694, lastError = self.exactly('+')
                self.considerError(lastError, None)
                self._trace('", ', (5659, 5662), self.input.position)
                _G_apply_695, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('ex1, ex2]\n  ', (5662, 5674), self.input.position)
                _G_apply_696, lastError = self._apply(self.rule_Expression7, "Expression7", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_696
                _G_python_698, lastError = eval(self._G_expr_697, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_698, self.currentError)
            def _G_or_699():
                self._trace(' WS Expressi', (5713, 5725), self.input.position)
                _G_apply_700, lastError = self._apply(self.rule_Expression6, "Expression6", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_700
                self._trace('ex2', (5729, 5732), self.input.position)
                _G_apply_701, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace(' -> ', (5732, 5736), self.input.position)
                _G_exactly_702, lastError = self.exactly('-')
                self.considerError(lastError, None)
                self._trace('["l', (5736, 5739), self.input.position)
                _G_apply_703, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('t",  ex1, ex', (5739, 5751), self.input.position)
                _G_apply_704, lastError = self._apply(self.rule_Expression7, "Expression7", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_704
                _G_python_706, lastError = eval(self._G_expr_705, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_706, self.currentError)
            def _G_or_707():
                self._trace(" '>'  WS Exp", (5790, 5802), self.input.position)
                _G_apply_708, lastError = self._apply(self.rule_Expression6, "Expression6", [])
                self.considerError(lastError, None)
                return (_G_apply_708, self.currentError)
            _G_or_709, lastError = self._or([_G_or_691, _G_or_699, _G_or_707])
            self.considerError(lastError, 'Expression7')
            return (_G_or_709, self.currentError)


        def rule_Expression6(self):
            _locals = {'self': self}
            self.locals['Expression6'] = _locals
            def _G_or_710():
                self._trace(' ["gt",  ex1', (5817, 5829), self.input.position)
                _G_apply_711, lastError = self._apply(self.rule_Expression5, "Expression5", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_711
                self._trace('2]\n', (5833, 5836), self.input.position)
                _G_apply_712, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('    ', (5836, 5840), self.input.position)
                _G_exactly_713, lastError = self.exactly('*')
                self.considerError(lastError, None)
                self._trace('   ', (5840, 5843), self.input.position)
                _G_apply_714, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('         | E', (5843, 5855), self.input.position)
                _G_apply_715, lastError = self._apply(self.rule_Expression6, "Expression6", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_715
                _G_python_717, lastError = eval(self._G_expr_716, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_717, self.currentError)
            def _G_or_718():
                self._trace(' -> ["lte", ', (5896, 5908), self.input.position)
                _G_apply_719, lastError = self._apply(self.rule_Expression5, "Expression5", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_719
                self._trace(' ex', (5912, 5915), self.input.position)
                _G_apply_720, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('2]\n ', (5915, 5919), self.input.position)
                _G_exactly_721, lastError = self.exactly('/')
                self.considerError(lastError, None)
                self._trace('   ', (5919, 5922), self.input.position)
                _G_apply_722, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('            ', (5922, 5934), self.input.position)
                _G_apply_723, lastError = self._apply(self.rule_Expression6, "Expression6", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_723
                _G_python_725, lastError = eval(self._G_expr_724, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_725, self.currentError)
            def _G_or_726():
                self._trace('ex2 -> ["gte', (5975, 5987), self.input.position)
                _G_apply_727, lastError = self._apply(self.rule_Expression5, "Expression5", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_727
                self._trace('x1,', (5991, 5994), self.input.position)
                _G_apply_728, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace(' ex2', (5994, 5998), self.input.position)
                _G_exactly_729, lastError = self.exactly('%')
                self.considerError(lastError, None)
                self._trace(']\n ', (5998, 6001), self.input.position)
                _G_apply_730, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('            ', (6001, 6013), self.input.position)
                _G_apply_731, lastError = self._apply(self.rule_Expression6, "Expression6", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_731
                _G_python_733, lastError = eval(self._G_expr_732, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_733, self.currentError)
            def _G_or_734():
                self._trace('ssion6:ex1 W', (6054, 6066), self.input.position)
                _G_apply_735, lastError = self._apply(self.rule_Expression5, "Expression5", [])
                self.considerError(lastError, None)
                return (_G_apply_735, self.currentError)
            _G_or_736, lastError = self._or([_G_or_710, _G_or_718, _G_or_726, _G_or_734])
            self.considerError(lastError, 'Expression6')
            return (_G_or_736, self.currentError)


        def rule_Expression5(self):
            _locals = {'self': self}
            self.locals['Expression5'] = _locals
            def _G_or_737():
                self._trace('sion7:ex2 ->', (6081, 6093), self.input.position)
                _G_apply_738, lastError = self._apply(self.rule_Expression4, "Expression4", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_738
                self._trace('dd"', (6097, 6100), self.input.position)
                _G_apply_739, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace(', ex', (6100, 6104), self.input.position)
                _G_exactly_740, lastError = self.exactly('^')
                self.considerError(lastError, None)
                self._trace('1, ', (6104, 6107), self.input.position)
                _G_apply_741, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('ex2]\n       ', (6107, 6119), self.input.position)
                _G_apply_742, lastError = self._apply(self.rule_Expression5, "Expression5", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_742
                _G_python_744, lastError = eval(self._G_expr_743, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_744, self.currentError)
            def _G_or_745():
                self._trace('pression7:ex', (6158, 6170), self.input.position)
                _G_apply_746, lastError = self._apply(self.rule_Expression4, "Expression4", [])
                self.considerError(lastError, None)
                return (_G_apply_746, self.currentError)
            _G_or_747, lastError = self._or([_G_or_737, _G_or_745])
            self.considerError(lastError, 'Expression5')
            return (_G_or_747, self.currentError)


        def rule_Expression4(self):
            _locals = {'self': self}
            self.locals['Expression4'] = _locals
            def _G_or_748():
                self._trace('1, e', (6185, 6189), self.input.position)
                _G_exactly_749, lastError = self.exactly('+')
                self.considerError(lastError, None)
                self._trace('x2]', (6189, 6192), self.input.position)
                _G_apply_750, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('\n           ', (6192, 6204), self.input.position)
                _G_apply_751, lastError = self._apply(self.rule_Expression4, "Expression4", [])
                self.considerError(lastError, None)
                return (_G_apply_751, self.currentError)
            def _G_or_752():
                self._trace('ion6', (6218, 6222), self.input.position)
                _G_exactly_753, lastError = self.exactly('-')
                self.considerError(lastError, None)
                self._trace('\n\n ', (6222, 6225), self.input.position)
                _G_apply_754, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('   Expressio', (6225, 6237), self.input.position)
                _G_apply_755, lastError = self._apply(self.rule_Expression4, "Expression4", [])
                self.considerError(lastError, None)
                _locals['ex'] = _G_apply_755
                _G_python_757, lastError = eval(self._G_expr_756, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_757, self.currentError)
            def _G_or_758():
                self._trace('ression6:ex2', (6271, 6283), self.input.position)
                _G_apply_759, lastError = self._apply(self.rule_Expression3, "Expression3", [])
                self.considerError(lastError, None)
                return (_G_apply_759, self.currentError)
            _G_or_760, lastError = self._or([_G_or_748, _G_or_752, _G_or_758])
            self.considerError(lastError, 'Expression4')
            return (_G_or_760, self.currentError)


        def rule_Expression3(self):
            _locals = {'self': self}
            self.locals['Expression3'] = _locals
            def _G_or_761():
                self._trace('x1, ex2]\n   ', (6298, 6310), self.input.position)
                _G_apply_762, lastError = self._apply(self.rule_Expression2, "Expression2", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_762
                def _G_many1_763():
                    def _G_or_764():
                        self._trace("ssion5:ex1 WS '/' W", (6330, 6349), self.input.position)
                        _G_apply_765, lastError = self._apply(self.rule_WS, "WS", [])
                        self.considerError(lastError, None)
                        self._trace('S Ex', (6349, 6353), self.input.position)
                        _G_exactly_766, lastError = self.exactly('[')
                        self.considerError(lastError, None)
                        self._trace('pression6:e', (6353, 6364), self.input.position)
                        _G_apply_767, lastError = self._apply(self.rule_Expression, "Expression", [])
                        self.considerError(lastError, None)
                        _locals['prop_name'] = _G_apply_767
                        self._trace('v", ', (6374, 6378), self.input.position)
                        _G_exactly_768, lastError = self.exactly(']')
                        self.considerError(lastError, None)
                        _G_python_770, lastError = eval(self._G_expr_769, self.globals, _locals), None
                        self.considerError(lastError, None)
                        return (_G_python_770, self.currentError)
                    def _G_or_771():
                        self._trace("' W", (6429, 6432), self.input.position)
                        _G_apply_772, lastError = self._apply(self.rule_WS, "WS", [])
                        self.considerError(lastError, None)
                        self._trace('S Ex', (6432, 6436), self.input.position)
                        _G_exactly_773, lastError = self.exactly('[')
                        self.considerError(lastError, None)
                        def _G_optional_774():
                            self._trace('pression6:e', (6436, 6447), self.input.position)
                            _G_apply_775, lastError = self._apply(self.rule_Expression, "Expression", [])
                            self.considerError(lastError, None)
                            return (_G_apply_775, self.currentError)
                        def _G_optional_776():
                            return (None, self.input.nullError())
                        _G_or_777, lastError = self._or([_G_optional_774, _G_optional_776])
                        self.considerError(lastError, None)
                        _locals['start'] = _G_or_777
                        self._trace('"mod"', (6454, 6459), self.input.position)
                        _G_exactly_778, lastError = self.exactly('..')
                        self.considerError(lastError, None)
                        def _G_optional_779():
                            self._trace(',   ex1, ex', (6459, 6470), self.input.position)
                            _G_apply_780, lastError = self._apply(self.rule_Expression, "Expression", [])
                            self.considerError(lastError, None)
                            return (_G_apply_780, self.currentError)
                        def _G_optional_781():
                            return (None, self.input.nullError())
                        _G_or_782, lastError = self._or([_G_optional_779, _G_optional_781])
                        self.considerError(lastError, None)
                        _locals['end'] = _G_or_782
                        self._trace('    ', (6475, 6479), self.input.position)
                        _G_exactly_783, lastError = self.exactly(']')
                        self.considerError(lastError, None)
                        _G_python_785, lastError = eval(self._G_expr_784, self.globals, _locals), None
                        self.considerError(lastError, None)
                        return (_G_python_785, self.currentError)
                    def _G_or_786():
                        def _G_or_787():
                            self._trace("pression4:ex1 WS '^' WS", (6524, 6547), self.input.position)
                            _G_apply_788, lastError = self._apply(self.rule_WS, "WS", [])
                            self.considerError(lastError, None)
                            self._trace(' Expr', (6547, 6552), self.input.position)
                            _G_exactly_789, lastError = self.exactly('=~')
                            self.considerError(lastError, None)
                            _G_python_790, lastError = ("regex"), None
                            self.considerError(lastError, None)
                            return (_G_python_790, self.currentError)
                        def _G_or_791():
                            self._trace('   ', (6585, 6588), self.input.position)
                            _G_apply_792, lastError = self._apply(self.rule_SP, "SP", [])
                            self.considerError(lastError, None)
                            self._trace('  ', (6588, 6590), self.input.position)
                            _G_apply_793, lastError = self._apply(self.rule_I, "I", [])
                            self.considerError(lastError, None)
                            self._trace('  ', (6590, 6592), self.input.position)
                            _G_apply_794, lastError = self._apply(self.rule_N, "N", [])
                            self.considerError(lastError, None)
                            _G_python_795, lastError = ("in"), None
                            self.considerError(lastError, None)
                            return (_G_python_795, self.currentError)
                        def _G_or_796():
                            self._trace('pre', (6622, 6625), self.input.position)
                            _G_apply_797, lastError = self._apply(self.rule_SP, "SP", [])
                            self.considerError(lastError, None)
                            self._trace('ss', (6625, 6627), self.input.position)
                            _G_apply_798, lastError = self._apply(self.rule_S, "S", [])
                            self.considerError(lastError, None)
                            self._trace('io', (6627, 6629), self.input.position)
                            _G_apply_799, lastError = self._apply(self.rule_T, "T", [])
                            self.considerError(lastError, None)
                            self._trace('n4', (6629, 6631), self.input.position)
                            _G_apply_800, lastError = self._apply(self.rule_A, "A", [])
                            self.considerError(lastError, None)
                            self._trace(' =', (6631, 6633), self.input.position)
                            _G_apply_801, lastError = self._apply(self.rule_R, "R", [])
                            self.considerError(lastError, None)
                            self._trace(" '", (6633, 6635), self.input.position)
                            _G_apply_802, lastError = self._apply(self.rule_T, "T", [])
                            self.considerError(lastError, None)
                            self._trace("+'", (6635, 6637), self.input.position)
                            _G_apply_803, lastError = self._apply(self.rule_S, "S", [])
                            self.considerError(lastError, None)
                            self._trace(' WS', (6637, 6640), self.input.position)
                            _G_apply_804, lastError = self._apply(self.rule_SP, "SP", [])
                            self.considerError(lastError, None)
                            self._trace(' E', (6640, 6642), self.input.position)
                            _G_apply_805, lastError = self._apply(self.rule_W, "W", [])
                            self.considerError(lastError, None)
                            self._trace('xp', (6642, 6644), self.input.position)
                            _G_apply_806, lastError = self._apply(self.rule_I, "I", [])
                            self.considerError(lastError, None)
                            self._trace('re', (6644, 6646), self.input.position)
                            _G_apply_807, lastError = self._apply(self.rule_T, "T", [])
                            self.considerError(lastError, None)
                            self._trace('ss', (6646, 6648), self.input.position)
                            _G_apply_808, lastError = self._apply(self.rule_H, "H", [])
                            self.considerError(lastError, None)
                            _G_python_809, lastError = ("starts_with"), None
                            self.considerError(lastError, None)
                            return (_G_python_809, self.currentError)
                        def _G_or_810():
                            self._trace('n4:', (6687, 6690), self.input.position)
                            _G_apply_811, lastError = self._apply(self.rule_SP, "SP", [])
                            self.considerError(lastError, None)
                            self._trace('ex', (6690, 6692), self.input.position)
                            _G_apply_812, lastError = self._apply(self.rule_E, "E", [])
                            self.considerError(lastError, None)
                            self._trace(' -', (6692, 6694), self.input.position)
                            _G_apply_813, lastError = self._apply(self.rule_N, "N", [])
                            self.considerError(lastError, None)
                            self._trace('> ', (6694, 6696), self.input.position)
                            _G_apply_814, lastError = self._apply(self.rule_D, "D", [])
                            self.considerError(lastError, None)
                            self._trace('["', (6696, 6698), self.input.position)
                            _G_apply_815, lastError = self._apply(self.rule_S, "S", [])
                            self.considerError(lastError, None)
                            self._trace('min', (6698, 6701), self.input.position)
                            _G_apply_816, lastError = self._apply(self.rule_SP, "SP", [])
                            self.considerError(lastError, None)
                            self._trace('us', (6701, 6703), self.input.position)
                            _G_apply_817, lastError = self._apply(self.rule_W, "W", [])
                            self.considerError(lastError, None)
                            self._trace('",', (6703, 6705), self.input.position)
                            _G_apply_818, lastError = self._apply(self.rule_I, "I", [])
                            self.considerError(lastError, None)
                            self._trace(' e', (6705, 6707), self.input.position)
                            _G_apply_819, lastError = self._apply(self.rule_T, "T", [])
                            self.considerError(lastError, None)
                            self._trace('x]', (6707, 6709), self.input.position)
                            _G_apply_820, lastError = self._apply(self.rule_H, "H", [])
                            self.considerError(lastError, None)
                            _G_python_821, lastError = ("ends_with"), None
                            self.considerError(lastError, None)
                            return (_G_python_821, self.currentError)
                        def _G_or_822():
                            self._trace('pre', (6747, 6750), self.input.position)
                            _G_apply_823, lastError = self._apply(self.rule_SP, "SP", [])
                            self.considerError(lastError, None)
                            self._trace('ss', (6750, 6752), self.input.position)
                            _G_apply_824, lastError = self._apply(self.rule_C, "C", [])
                            self.considerError(lastError, None)
                            self._trace('io', (6752, 6754), self.input.position)
                            _G_apply_825, lastError = self._apply(self.rule_O, "O", [])
                            self.considerError(lastError, None)
                            self._trace('n3', (6754, 6756), self.input.position)
                            _G_apply_826, lastError = self._apply(self.rule_N, "N", [])
                            self.considerError(lastError, None)
                            self._trace(' =', (6756, 6758), self.input.position)
                            _G_apply_827, lastError = self._apply(self.rule_T, "T", [])
                            self.considerError(lastError, None)
                            self._trace(' E', (6758, 6760), self.input.position)
                            _G_apply_828, lastError = self._apply(self.rule_A, "A", [])
                            self.considerError(lastError, None)
                            self._trace('xp', (6760, 6762), self.input.position)
                            _G_apply_829, lastError = self._apply(self.rule_I, "I", [])
                            self.considerError(lastError, None)
                            self._trace('re', (6762, 6764), self.input.position)
                            _G_apply_830, lastError = self._apply(self.rule_N, "N", [])
                            self.considerError(lastError, None)
                            self._trace('ss', (6764, 6766), self.input.position)
                            _G_apply_831, lastError = self._apply(self.rule_S, "S", [])
                            self.considerError(lastError, None)
                            _G_python_832, lastError = ("contains"), None
                            self.considerError(lastError, None)
                            return (_G_python_832, self.currentError)
                        _G_or_833, lastError = self._or([_G_or_787, _G_or_791, _G_or_796, _G_or_810, _G_or_822])
                        self.considerError(lastError, None)
                        _locals['operator'] = _G_or_833
                        self._trace('   ', (6808, 6811), self.input.position)
                        _G_apply_834, lastError = self._apply(self.rule_WS, "WS", [])
                        self.considerError(lastError, None)
                        self._trace("    WS '[' E", (6811, 6823), self.input.position)
                        _G_apply_835, lastError = self._apply(self.rule_Expression2, "Expression2", [])
                        self.considerError(lastError, None)
                        _locals['ex2'] = _G_apply_835
                        _G_python_837, lastError = eval(self._G_expr_836, self.globals, _locals), None
                        self.considerError(lastError, None)
                        return (_G_python_837, self.currentError)
                    def _G_or_838():
                        self._trace('up"', (6864, 6867), self.input.position)
                        _G_apply_839, lastError = self._apply(self.rule_SP, "SP", [])
                        self.considerError(lastError, None)
                        self._trace(', ', (6867, 6869), self.input.position)
                        _G_apply_840, lastError = self._apply(self.rule_I, "I", [])
                        self.considerError(lastError, None)
                        self._trace('pr', (6869, 6871), self.input.position)
                        _G_apply_841, lastError = self._apply(self.rule_S, "S", [])
                        self.considerError(lastError, None)
                        self._trace('op_', (6871, 6874), self.input.position)
                        _G_apply_842, lastError = self._apply(self.rule_SP, "SP", [])
                        self.considerError(lastError, None)
                        self._trace('na', (6874, 6876), self.input.position)
                        _G_apply_843, lastError = self._apply(self.rule_N, "N", [])
                        self.considerError(lastError, None)
                        self._trace('me', (6876, 6878), self.input.position)
                        _G_apply_844, lastError = self._apply(self.rule_U, "U", [])
                        self.considerError(lastError, None)
                        self._trace(']\n', (6878, 6880), self.input.position)
                        _G_apply_845, lastError = self._apply(self.rule_L, "L", [])
                        self.considerError(lastError, None)
                        self._trace('  ', (6880, 6882), self.input.position)
                        _G_apply_846, lastError = self._apply(self.rule_L, "L", [])
                        self.considerError(lastError, None)
                        _G_python_847, lastError = (["is_null"]), None
                        self.considerError(lastError, None)
                        return (_G_python_847, self.currentError)
                    def _G_or_848():
                        self._trace('ion', (6916, 6919), self.input.position)
                        _G_apply_849, lastError = self._apply(self.rule_SP, "SP", [])
                        self.considerError(lastError, None)
                        self._trace('?:', (6919, 6921), self.input.position)
                        _G_apply_850, lastError = self._apply(self.rule_I, "I", [])
                        self.considerError(lastError, None)
                        self._trace('st', (6921, 6923), self.input.position)
                        _G_apply_851, lastError = self._apply(self.rule_S, "S", [])
                        self.considerError(lastError, None)
                        self._trace('art', (6923, 6926), self.input.position)
                        _G_apply_852, lastError = self._apply(self.rule_SP, "SP", [])
                        self.considerError(lastError, None)
                        self._trace(" '", (6926, 6928), self.input.position)
                        _G_apply_853, lastError = self._apply(self.rule_N, "N", [])
                        self.considerError(lastError, None)
                        self._trace('..', (6928, 6930), self.input.position)
                        _G_apply_854, lastError = self._apply(self.rule_O, "O", [])
                        self.considerError(lastError, None)
                        self._trace("' ", (6930, 6932), self.input.position)
                        _G_apply_855, lastError = self._apply(self.rule_T, "T", [])
                        self.considerError(lastError, None)
                        self._trace('Exp', (6932, 6935), self.input.position)
                        _G_apply_856, lastError = self._apply(self.rule_SP, "SP", [])
                        self.considerError(lastError, None)
                        self._trace('re', (6935, 6937), self.input.position)
                        _G_apply_857, lastError = self._apply(self.rule_N, "N", [])
                        self.considerError(lastError, None)
                        self._trace('ss', (6937, 6939), self.input.position)
                        _G_apply_858, lastError = self._apply(self.rule_U, "U", [])
                        self.considerError(lastError, None)
                        self._trace('io', (6939, 6941), self.input.position)
                        _G_apply_859, lastError = self._apply(self.rule_L, "L", [])
                        self.considerError(lastError, None)
                        self._trace('n?', (6941, 6943), self.input.position)
                        _G_apply_860, lastError = self._apply(self.rule_L, "L", [])
                        self.considerError(lastError, None)
                        _G_python_861, lastError = (["is_not_null"]), None
                        self.considerError(lastError, None)
                        return (_G_python_861, self.currentError)
                    _G_or_862, lastError = self._or([_G_or_764, _G_or_771, _G_or_786, _G_or_838, _G_or_848])
                    self.considerError(lastError, None)
                    return (_G_or_862, self.currentError)
                _G_many1_863, lastError = self.many(_G_many1_763, _G_many1_763())
                self.considerError(lastError, None)
                _locals['c'] = _G_many1_863
                _G_python_865, lastError = eval(self._G_expr_864, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_865, self.currentError)
            def _G_or_866():
                self._trace(" WS '=~' -> ", (7024, 7036), self.input.position)
                _G_apply_867, lastError = self._apply(self.rule_Expression2, "Expression2", [])
                self.considerError(lastError, None)
                return (_G_apply_867, self.currentError)
            _G_or_868, lastError = self._or([_G_or_761, _G_or_866])
            self.considerError(lastError, 'Expression3')
            return (_G_or_868, self.currentError)


        def rule_Expression2(self):
            _locals = {'self': self}
            self.locals['Expression2'] = _locals
            def _G_or_869():
                self._trace('     ', (7051, 7056), self.input.position)
                _G_apply_870, lastError = self._apply(self.rule_Atom, "Atom", [])
                self.considerError(lastError, None)
                _locals['a'] = _G_apply_870
                def _G_many1_871():
                    def _G_or_872():
                        self._trace('        | SP I', (7060, 7074), self.input.position)
                        _G_apply_873, lastError = self._apply(self.rule_PropertyLookup, "PropertyLookup", [])
                        self.considerError(lastError, None)
                        return (_G_apply_873, self.currentError)
                    def _G_or_874():
                        self._trace(' -> "in"\n  ', (7076, 7087), self.input.position)
                        _G_apply_875, lastError = self._apply(self.rule_NodeLabels, "NodeLabels", [])
                        self.considerError(lastError, None)
                        return (_G_apply_875, self.currentError)
                    _G_or_876, lastError = self._or([_G_or_872, _G_or_874])
                    self.considerError(lastError, None)
                    return (_G_or_876, self.currentError)
                _G_many1_877, lastError = self.many(_G_many1_871, _G_many1_871())
                self.considerError(lastError, None)
                _locals['c'] = _G_many1_877
                _G_python_879, lastError = eval(self._G_expr_878, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_879, self.currentError)
            def _G_or_880():
                self._trace(' T H ', (7132, 7137), self.input.position)
                _G_apply_881, lastError = self._apply(self.rule_Atom, "Atom", [])
                self.considerError(lastError, None)
                return (_G_apply_881, self.currentError)
            _G_or_882, lastError = self._or([_G_or_869, _G_or_880])
            self.considerError(lastError, 'Expression2')
            return (_G_or_882, self.currentError)


        def rule_Atom(self):
            _locals = {'self': self}
            self.locals['Atom'] = _locals
            def _G_or_883():
                self._trace('ts_with"\n     ', (7145, 7159), self.input.position)
                _G_apply_884, lastError = self._apply(self.rule_NumberLiteral, "NumberLiteral", [])
                self.considerError(lastError, None)
                return (_G_apply_884, self.currentError)
            def _G_or_885():
                self._trace('            | ', (7166, 7180), self.input.position)
                _G_apply_886, lastError = self._apply(self.rule_StringLiteral, "StringLiteral", [])
                self.considerError(lastError, None)
                return (_G_apply_886, self.currentError)
            def _G_or_887():
                self._trace('D S SP W I', (7187, 7197), self.input.position)
                _G_apply_888, lastError = self._apply(self.rule_Parameter, "Parameter", [])
                self.considerError(lastError, None)
                return (_G_apply_888, self.currentError)
            def _G_or_889():
                self._trace('> ', (7204, 7206), self.input.position)
                _G_apply_890, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                self._trace('"e', (7206, 7208), self.input.position)
                _G_apply_891, lastError = self._apply(self.rule_R, "R", [])
                self.considerError(lastError, None)
                self._trace('nd', (7208, 7210), self.input.position)
                _G_apply_892, lastError = self._apply(self.rule_U, "U", [])
                self.considerError(lastError, None)
                self._trace('s_', (7210, 7212), self.input.position)
                _G_apply_893, lastError = self._apply(self.rule_E, "E", [])
                self.considerError(lastError, None)
                _G_python_894, lastError = (["Literal", True]), None
                self.considerError(lastError, None)
                return (_G_python_894, self.currentError)
            def _G_or_895():
                self._trace('  ', (7240, 7242), self.input.position)
                _G_apply_896, lastError = self._apply(self.rule_F, "F", [])
                self.considerError(lastError, None)
                self._trace('| ', (7242, 7244), self.input.position)
                _G_apply_897, lastError = self._apply(self.rule_A, "A", [])
                self.considerError(lastError, None)
                self._trace('SP', (7244, 7246), self.input.position)
                _G_apply_898, lastError = self._apply(self.rule_L, "L", [])
                self.considerError(lastError, None)
                self._trace(' C', (7246, 7248), self.input.position)
                _G_apply_899, lastError = self._apply(self.rule_S, "S", [])
                self.considerError(lastError, None)
                self._trace(' O', (7248, 7250), self.input.position)
                _G_apply_900, lastError = self._apply(self.rule_E, "E", [])
                self.considerError(lastError, None)
                _G_python_901, lastError = (["Literal", False]), None
                self.considerError(lastError, None)
                return (_G_python_901, self.currentError)
            def _G_or_902():
                self._trace('  ', (7279, 7281), self.input.position)
                _G_apply_903, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace('  ', (7281, 7283), self.input.position)
                _G_apply_904, lastError = self._apply(self.rule_U, "U", [])
                self.considerError(lastError, None)
                self._trace('  ', (7283, 7285), self.input.position)
                _G_apply_905, lastError = self._apply(self.rule_L, "L", [])
                self.considerError(lastError, None)
                self._trace('  ', (7285, 7287), self.input.position)
                _G_apply_906, lastError = self._apply(self.rule_L, "L", [])
                self.considerError(lastError, None)
                _G_python_907, lastError = (["Literal", None]), None
                self.considerError(lastError, None)
                return (_G_python_907, self.currentError)
            def _G_or_908():
                self._trace('ression2:ex2 ->', (7315, 7330), self.input.position)
                _G_apply_909, lastError = self._apply(self.rule_CaseExpression, "CaseExpression", [])
                self.considerError(lastError, None)
                return (_G_apply_909, self.currentError)
            def _G_or_910():
                self._trace('to', (7337, 7339), self.input.position)
                _G_apply_911, lastError = self._apply(self.rule_C, "C", [])
                self.considerError(lastError, None)
                self._trace('r,', (7339, 7341), self.input.position)
                _G_apply_912, lastError = self._apply(self.rule_O, "O", [])
                self.considerError(lastError, None)
                self._trace(' e', (7341, 7343), self.input.position)
                _G_apply_913, lastError = self._apply(self.rule_U, "U", [])
                self.considerError(lastError, None)
                self._trace('x2', (7343, 7345), self.input.position)
                _G_apply_914, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace(']\n', (7345, 7347), self.input.position)
                _G_apply_915, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                self._trace('    ', (7347, 7351), self.input.position)
                _G_exactly_916, lastError = self.exactly('(')
                self.considerError(lastError, None)
                self._trace('    ', (7351, 7355), self.input.position)
                _G_exactly_917, lastError = self.exactly('*')
                self.considerError(lastError, None)
                self._trace('    ', (7355, 7359), self.input.position)
                _G_exactly_918, lastError = self.exactly(')')
                self.considerError(lastError, None)
                _G_python_919, lastError = (["count *"]), None
                self.considerError(lastError, None)
                return (_G_python_919, self.currentError)
            def _G_or_920():
                self._trace('U L L  -> [', (7381, 7392), self.input.position)
                _G_apply_921, lastError = self._apply(self.rule_MapLiteral, "MapLiteral", [])
                self.considerError(lastError, None)
                return (_G_apply_921, self.currentError)
            def _G_or_922():
                self._trace('l"]\n              ', (7399, 7417), self.input.position)
                _G_apply_923, lastError = self._apply(self.rule_ListComprehension, "ListComprehension", [])
                self.considerError(lastError, None)
                return (_G_apply_923, self.currentError)
            def _G_or_924():
                self._trace(' SP ', (7424, 7428), self.input.position)
                _G_exactly_925, lastError = self.exactly('[')
                self.considerError(lastError, None)
                def _G_or_926():
                    self._trace('P N U L L -> ["is_n', (7442, 7461), self.input.position)
                    _G_apply_927, lastError = self._apply(self.rule_WS, "WS", [])
                    self.considerError(lastError, None)
                    self._trace('ot_null"]\n ', (7461, 7472), self.input.position)
                    _G_apply_928, lastError = self._apply(self.rule_Expression, "Expression", [])
                    self.considerError(lastError, None)
                    _locals['head'] = _G_apply_928
                    self._trace('   ', (7477, 7480), self.input.position)
                    _G_apply_929, lastError = self._apply(self.rule_WS, "WS", [])
                    self.considerError(lastError, None)
                    def _G_many_930():
                        self._trace('"Ex', (7498, 7501), self.input.position)
                        _G_exactly_931, lastError = self.exactly(',')
                        self.considerError(lastError, None)
                        self._trace('pre', (7501, 7504), self.input.position)
                        _G_apply_932, lastError = self._apply(self.rule_WS, "WS", [])
                        self.considerError(lastError, None)
                        self._trace('ssion3", ex', (7504, 7515), self.input.position)
                        _G_apply_933, lastError = self._apply(self.rule_Expression, "Expression", [])
                        self.considerError(lastError, None)
                        _locals['item'] = _G_apply_933
                        self._trace('\n  ', (7520, 7523), self.input.position)
                        _G_apply_934, lastError = self._apply(self.rule_WS, "WS", [])
                        self.considerError(lastError, None)
                        _G_python_936, lastError = eval(self._G_expr_935, self.globals, _locals), None
                        self.considerError(lastError, None)
                        return (_G_python_936, self.currentError)
                    _G_many_937, lastError = self.many(_G_many_930)
                    self.considerError(lastError, None)
                    _locals['tail'] = _G_many_937
                    _G_python_938, lastError = eval(self._G_expr_423, self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_938, self.currentError)
                def _G_or_939():
                    _G_python_940, lastError = ([]), None
                    self.considerError(lastError, None)
                    return (_G_python_940, self.currentError)
                _G_or_941, lastError = self._or([_G_or_926, _G_or_939])
                self.considerError(lastError, None)
                _locals['ex'] = _G_or_941
                self._trace(', a, c]\n    ', (7629, 7641), self.input.position)
                _G_exactly_942, lastError = self.exactly(']')
                self.considerError(lastError, None)
                _G_python_944, lastError = eval(self._G_expr_943, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_944, self.currentError)
            def _G_or_945():
                self._trace('  ', (7664, 7666), self.input.position)
                _G_apply_946, lastError = self._apply(self.rule_F, "F", [])
                self.considerError(lastError, None)
                self._trace(' A', (7666, 7668), self.input.position)
                _G_apply_947, lastError = self._apply(self.rule_I, "I", [])
                self.considerError(lastError, None)
                self._trace('to', (7668, 7670), self.input.position)
                _G_apply_948, lastError = self._apply(self.rule_L, "L", [])
                self.considerError(lastError, None)
                self._trace('m ', (7670, 7672), self.input.position)
                _G_apply_949, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                self._trace('= ', (7672, 7674), self.input.position)
                _G_apply_950, lastError = self._apply(self.rule_E, "E", [])
                self.considerError(lastError, None)
                self._trace('Nu', (7674, 7676), self.input.position)
                _G_apply_951, lastError = self._apply(self.rule_R, "R", [])
                self.considerError(lastError, None)
                self._trace('mbe', (7676, 7679), self.input.position)
                _G_apply_952, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('rLit', (7679, 7683), self.input.position)
                _G_exactly_953, lastError = self.exactly('(')
                self.considerError(lastError, None)
                self._trace('era', (7683, 7686), self.input.position)
                _G_apply_954, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('l\n         | Stri', (7686, 7703), self.input.position)
                _G_apply_955, lastError = self._apply(self.rule_FilterExpression, "FilterExpression", [])
                self.considerError(lastError, None)
                _locals['fex'] = _G_apply_955
                self._trace('ter', (7707, 7710), self.input.position)
                _G_apply_956, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('al\n ', (7710, 7714), self.input.position)
                _G_exactly_957, lastError = self.exactly(')')
                self.considerError(lastError, None)
                _G_python_959, lastError = eval(self._G_expr_958, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_959, self.currentError)
            def _G_or_960():
                self._trace('  ', (7740, 7742), self.input.position)
                _G_apply_961, lastError = self._apply(self.rule_E, "E", [])
                self.considerError(lastError, None)
                self._trace(' |', (7742, 7744), self.input.position)
                _G_apply_962, lastError = self._apply(self.rule_X, "X", [])
                self.considerError(lastError, None)
                self._trace(' T', (7744, 7746), self.input.position)
                _G_apply_963, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                self._trace(' R', (7746, 7748), self.input.position)
                _G_apply_964, lastError = self._apply(self.rule_R, "R", [])
                self.considerError(lastError, None)
                self._trace(' U', (7748, 7750), self.input.position)
                _G_apply_965, lastError = self._apply(self.rule_A, "A", [])
                self.considerError(lastError, None)
                self._trace(' E', (7750, 7752), self.input.position)
                _G_apply_966, lastError = self._apply(self.rule_C, "C", [])
                self.considerError(lastError, None)
                self._trace(' -', (7752, 7754), self.input.position)
                _G_apply_967, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                self._trace('> [', (7754, 7757), self.input.position)
                _G_apply_968, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('"Lit', (7757, 7761), self.input.position)
                _G_exactly_969, lastError = self.exactly('(')
                self.considerError(lastError, None)
                self._trace('era', (7761, 7764), self.input.position)
                _G_apply_970, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('l", True]\n       ', (7764, 7781), self.input.position)
                _G_apply_971, lastError = self._apply(self.rule_FilterExpression, "FilterExpression", [])
                self.considerError(lastError, None)
                _locals['fex'] = _G_apply_971
                self._trace('F A', (7785, 7788), self.input.position)
                _G_apply_972, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                def _G_optional_973():
                    self._trace(' S', (7790, 7792), self.input.position)
                    _G_apply_974, lastError = self._apply(self.rule_WS, "WS", [])
                    self.considerError(lastError, None)
                    self._trace(' E -', (7792, 7796), self.input.position)
                    _G_exactly_975, lastError = self.exactly('|')
                    self.considerError(lastError, None)
                    self._trace('> ["Literal', (7796, 7807), self.input.position)
                    _G_apply_976, lastError = self._apply(self.rule_Expression, "Expression", [])
                    self.considerError(lastError, None)
                    return (_G_apply_976, self.currentError)
                def _G_optional_977():
                    return (None, self.input.nullError())
                _G_or_978, lastError = self._or([_G_optional_973, _G_optional_977])
                self.considerError(lastError, None)
                _locals['ex'] = _G_or_978
                self._trace('lse]', (7812, 7816), self.input.position)
                _G_exactly_979, lastError = self.exactly(')')
                self.considerError(lastError, None)
                _G_python_981, lastError = eval(self._G_expr_980, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_981, self.currentError)
            def _G_or_982():
                self._trace('l"', (7847, 7849), self.input.position)
                _G_apply_983, lastError = self._apply(self.rule_A, "A", [])
                self.considerError(lastError, None)
                self._trace(', ', (7849, 7851), self.input.position)
                _G_apply_984, lastError = self._apply(self.rule_L, "L", [])
                self.considerError(lastError, None)
                self._trace('No', (7851, 7853), self.input.position)
                _G_apply_985, lastError = self._apply(self.rule_L, "L", [])
                self.considerError(lastError, None)
                self._trace('ne]', (7853, 7856), self.input.position)
                _G_apply_986, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('\n   ', (7856, 7860), self.input.position)
                _G_exactly_987, lastError = self.exactly('(')
                self.considerError(lastError, None)
                self._trace('   ', (7860, 7863), self.input.position)
                _G_apply_988, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('   | CaseExpressi', (7863, 7880), self.input.position)
                _G_apply_989, lastError = self._apply(self.rule_FilterExpression, "FilterExpression", [])
                self.considerError(lastError, None)
                _locals['fex'] = _G_apply_989
                self._trace('   ', (7884, 7887), self.input.position)
                _G_apply_990, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('    ', (7887, 7891), self.input.position)
                _G_exactly_991, lastError = self.exactly(')')
                self.considerError(lastError, None)
                _G_python_993, lastError = eval(self._G_expr_992, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_993, self.currentError)
            def _G_or_994():
                self._trace("' ", (7914, 7916), self.input.position)
                _G_apply_995, lastError = self._apply(self.rule_A, "A", [])
                self.considerError(lastError, None)
                self._trace('->', (7916, 7918), self.input.position)
                _G_apply_996, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace(' [', (7918, 7920), self.input.position)
                _G_apply_997, lastError = self._apply(self.rule_Y, "Y", [])
                self.considerError(lastError, None)
                self._trace('"co', (7920, 7923), self.input.position)
                _G_apply_998, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('unt ', (7923, 7927), self.input.position)
                _G_exactly_999, lastError = self.exactly('(')
                self.considerError(lastError, None)
                self._trace('*"]', (7927, 7930), self.input.position)
                _G_apply_1000, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('\n         | MapLi', (7930, 7947), self.input.position)
                _G_apply_1001, lastError = self._apply(self.rule_FilterExpression, "FilterExpression", [])
                self.considerError(lastError, None)
                _locals['fex'] = _G_apply_1001
                self._trace('l\n ', (7951, 7954), self.input.position)
                _G_apply_1002, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('    ', (7954, 7958), self.input.position)
                _G_exactly_1003, lastError = self.exactly(')')
                self.considerError(lastError, None)
                _G_python_1005, lastError = eval(self._G_expr_1004, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_1005, self.currentError)
            def _G_or_1006():
                self._trace('\n ', (7981, 7983), self.input.position)
                _G_apply_1007, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace('  ', (7983, 7985), self.input.position)
                _G_apply_1008, lastError = self._apply(self.rule_O, "O", [])
                self.considerError(lastError, None)
                self._trace('  ', (7985, 7987), self.input.position)
                _G_apply_1009, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace('  ', (7987, 7989), self.input.position)
                _G_apply_1010, lastError = self._apply(self.rule_E, "E", [])
                self.considerError(lastError, None)
                self._trace('  |', (7989, 7992), self.input.position)
                _G_apply_1011, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace(" '['", (7992, 7996), self.input.position)
                _G_exactly_1012, lastError = self.exactly('(')
                self.considerError(lastError, None)
                self._trace('\n  ', (7996, 7999), self.input.position)
                _G_apply_1013, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('              (\n ', (7999, 8016), self.input.position)
                _G_apply_1014, lastError = self._apply(self.rule_FilterExpression, "FilterExpression", [])
                self.considerError(lastError, None)
                _locals['fex'] = _G_apply_1014
                self._trace('   ', (8020, 8023), self.input.position)
                _G_apply_1015, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('    ', (8023, 8027), self.input.position)
                _G_exactly_1016, lastError = self.exactly(')')
                self.considerError(lastError, None)
                _G_python_1018, lastError = eval(self._G_expr_1017, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_1018, self.currentError)
            def _G_or_1019():
                self._trace('ad', (8051, 8053), self.input.position)
                _G_apply_1020, lastError = self._apply(self.rule_S, "S", [])
                self.considerError(lastError, None)
                self._trace(' W', (8053, 8055), self.input.position)
                _G_apply_1021, lastError = self._apply(self.rule_I, "I", [])
                self.considerError(lastError, None)
                self._trace('S\n', (8055, 8057), self.input.position)
                _G_apply_1022, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace('  ', (8057, 8059), self.input.position)
                _G_apply_1023, lastError = self._apply(self.rule_G, "G", [])
                self.considerError(lastError, None)
                self._trace('  ', (8059, 8061), self.input.position)
                _G_apply_1024, lastError = self._apply(self.rule_L, "L", [])
                self.considerError(lastError, None)
                self._trace('  ', (8061, 8063), self.input.position)
                _G_apply_1025, lastError = self._apply(self.rule_E, "E", [])
                self.considerError(lastError, None)
                self._trace('   ', (8063, 8066), self.input.position)
                _G_apply_1026, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('    ', (8066, 8070), self.input.position)
                _G_exactly_1027, lastError = self.exactly('(')
                self.considerError(lastError, None)
                self._trace('   ', (8070, 8073), self.input.position)
                _G_apply_1028, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace("    (',' WS Expre", (8073, 8090), self.input.position)
                _G_apply_1029, lastError = self._apply(self.rule_FilterExpression, "FilterExpression", [])
                self.considerError(lastError, None)
                _locals['fex'] = _G_apply_1029
                self._trace('n:i', (8094, 8097), self.input.position)
                _G_apply_1030, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('tem ', (8097, 8101), self.input.position)
                _G_exactly_1031, lastError = self.exactly(')')
                self.considerError(lastError, None)
                _G_python_1033, lastError = eval(self._G_expr_1032, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_1033, self.currentError)
            def _G_or_1034():
                self._trace('     )*:tail -> [head', (8127, 8148), self.input.position)
                _G_apply_1035, lastError = self._apply(self.rule_RelationshipsPattern, "RelationshipsPattern", [])
                self.considerError(lastError, None)
                return (_G_apply_1035, self.currentError)
            def _G_or_1036():
                self._trace('l\n                    |\n  ', (8155, 8181), self.input.position)
                _G_apply_1037, lastError = self._apply(self.rule_GraphRelationshipsPattern, "GraphRelationshipsPattern", [])
                self.considerError(lastError, None)
                return (_G_apply_1037, self.currentError)
            def _G_or_1038():
                self._trace('           -> []\n       ', (8188, 8212), self.input.position)
                _G_apply_1039, lastError = self._apply(self.rule_parenthesizedExpression, "parenthesizedExpression", [])
                self.considerError(lastError, None)
                return (_G_apply_1039, self.currentError)
            def _G_or_1040():
                self._trace('  ):ex\n            ', (8219, 8238), self.input.position)
                _G_apply_1041, lastError = self._apply(self.rule_FunctionInvocation, "FunctionInvocation", [])
                self.considerError(lastError, None)
                return (_G_apply_1041, self.currentError)
            def _G_or_1042():
                self._trace('["List", ', (8245, 8254), self.input.position)
                _G_apply_1043, lastError = self._apply(self.rule_Variable, "Variable", [])
                self.considerError(lastError, None)
                return (_G_apply_1043, self.currentError)
            _G_or_1044, lastError = self._or([_G_or_883, _G_or_885, _G_or_887, _G_or_889, _G_or_895, _G_or_902, _G_or_908, _G_or_910, _G_or_920, _G_or_922, _G_or_924, _G_or_945, _G_or_960, _G_or_982, _G_or_994, _G_or_1006, _G_or_1019, _G_or_1034, _G_or_1036, _G_or_1038, _G_or_1040, _G_or_1042])
            self.considerError(lastError, 'Atom')
            return (_G_or_1044, self.currentError)


        def rule_parenthesizedExpression(self):
            _locals = {'self': self}
            self.locals['parenthesizedExpression'] = _locals
            self._trace("WS '", (8281, 8285), self.input.position)
            _G_exactly_1045, lastError = self.exactly('(')
            self.considerError(lastError, 'parenthesizedExpression')
            self._trace("(' ", (8285, 8288), self.input.position)
            _G_apply_1046, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'parenthesizedExpression')
            self._trace('WS FilterEx', (8288, 8299), self.input.position)
            _G_apply_1047, lastError = self._apply(self.rule_Expression, "Expression", [])
            self.considerError(lastError, 'parenthesizedExpression')
            _locals['ex'] = _G_apply_1047
            self._trace('ssi', (8302, 8305), self.input.position)
            _G_apply_1048, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'parenthesizedExpression')
            self._trace('on:f', (8305, 8309), self.input.position)
            _G_exactly_1049, lastError = self.exactly(')')
            self.considerError(lastError, 'parenthesizedExpression')
            _G_python_1051, lastError = eval(self._G_expr_1050, self.globals, _locals), None
            self.considerError(lastError, 'parenthesizedExpression')
            return (_G_python_1051, self.currentError)


        def rule_RelationshipsPattern(self):
            _locals = {'self': self}
            self.locals['RelationshipsPattern'] = _locals
            self._trace('        | E ', (8339, 8351), self.input.position)
            _G_apply_1052, lastError = self._apply(self.rule_NodePattern, "NodePattern", [])
            self.considerError(lastError, 'RelationshipsPattern')
            _locals['np'] = _G_apply_1052
            def _G_optional_1053():
                self._trace(' A', (8356, 8358), self.input.position)
                _G_apply_1054, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace(" C T WS '(' WS Filte", (8358, 8378), self.input.position)
                _G_apply_1055, lastError = self._apply(self.rule_PatternElementChain, "PatternElementChain", [])
                self.considerError(lastError, None)
                return (_G_apply_1055, self.currentError)
            def _G_optional_1056():
                return (None, self.input.nullError())
            _G_or_1057, lastError = self._or([_G_optional_1053, _G_optional_1056])
            self.considerError(lastError, 'RelationshipsPattern')
            _locals['pec'] = _G_or_1057
            _G_python_1059, lastError = eval(self._G_expr_1058, self.globals, _locals), None
            self.considerError(lastError, 'RelationshipsPattern')
            return (_G_python_1059, self.currentError)


        def rule_GraphRelationshipsPattern(self):
            _locals = {'self': self}
            self.locals['GraphRelationshipsPattern'] = _locals
            self._trace('        |', (8450, 8459), self.input.position)
            _G_apply_1060, lastError = self._apply(self.rule_Variable, "Variable", [])
            self.considerError(lastError, 'GraphRelationshipsPattern')
            _locals['v'] = _G_apply_1060
            self._trace(' L L', (8461, 8465), self.input.position)
            _G_exactly_1061, lastError = self.exactly(':')
            self.considerError(lastError, 'GraphRelationshipsPattern')
            self._trace(' WS', (8465, 8468), self.input.position)
            _G_apply_1062, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'GraphRelationshipsPattern')
            self._trace(" '(' WS Filt", (8468, 8480), self.input.position)
            _G_apply_1063, lastError = self._apply(self.rule_NodePattern, "NodePattern", [])
            self.considerError(lastError, 'GraphRelationshipsPattern')
            _locals['np'] = _G_apply_1063
            def _G_optional_1064():
                self._trace('re', (8485, 8487), self.input.position)
                _G_apply_1065, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace("ssion:fex WS ')' -> ", (8487, 8507), self.input.position)
                _G_apply_1066, lastError = self._apply(self.rule_PatternElementChain, "PatternElementChain", [])
                self.considerError(lastError, None)
                return (_G_apply_1066, self.currentError)
            def _G_optional_1067():
                return (None, self.input.nullError())
            _G_or_1068, lastError = self._or([_G_optional_1064, _G_optional_1067])
            self.considerError(lastError, 'GraphRelationshipsPattern')
            _locals['pec'] = _G_or_1068
            _G_python_1070, lastError = eval(self._G_expr_1069, self.globals, _locals), None
            self.considerError(lastError, 'GraphRelationshipsPattern')
            return (_G_python_1070, self.currentError)


        def rule_FilterExpression(self):
            _locals = {'self': self}
            self.locals['FilterExpression'] = _locals
            self._trace('["Any", f', (8578, 8587), self.input.position)
            _G_apply_1071, lastError = self._apply(self.rule_IdInColl, "IdInColl", [])
            self.considerError(lastError, 'FilterExpression')
            _locals['i'] = _G_apply_1071
            def _G_optional_1072():
                self._trace('  ', (8591, 8593), self.input.position)
                _G_apply_1073, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('      ', (8593, 8599), self.input.position)
                _G_apply_1074, lastError = self._apply(self.rule_Where, "Where", [])
                self.considerError(lastError, None)
                return (_G_apply_1074, self.currentError)
            def _G_optional_1075():
                return (None, self.input.nullError())
            _G_or_1076, lastError = self._or([_G_optional_1072, _G_optional_1075])
            self.considerError(lastError, 'FilterExpression')
            _locals['w'] = _G_or_1076
            _G_python_1078, lastError = eval(self._G_expr_1077, self.globals, _locals), None
            self.considerError(lastError, 'FilterExpression')
            return (_G_python_1078, self.currentError)


        def rule_IdInColl(self):
            _locals = {'self': self}
            self.locals['IdInColl'] = _locals
            self._trace(')\' -> ["N', (8645, 8654), self.input.position)
            _G_apply_1079, lastError = self._apply(self.rule_Variable, "Variable", [])
            self.considerError(lastError, 'IdInColl')
            _locals['v'] = _G_apply_1079
            self._trace('e",', (8656, 8659), self.input.position)
            _G_apply_1080, lastError = self._apply(self.rule_SP, "SP", [])
            self.considerError(lastError, 'IdInColl')
            self._trace(' f', (8659, 8661), self.input.position)
            _G_apply_1081, lastError = self._apply(self.rule_I, "I", [])
            self.considerError(lastError, 'IdInColl')
            self._trace('ex', (8661, 8663), self.input.position)
            _G_apply_1082, lastError = self._apply(self.rule_N, "N", [])
            self.considerError(lastError, 'IdInColl')
            self._trace(']\n ', (8663, 8666), self.input.position)
            _G_apply_1083, lastError = self._apply(self.rule_SP, "SP", [])
            self.considerError(lastError, 'IdInColl')
            self._trace('        | S', (8666, 8677), self.input.position)
            _G_apply_1084, lastError = self._apply(self.rule_Expression, "Expression", [])
            self.considerError(lastError, 'IdInColl')
            _locals['ex'] = _G_apply_1084
            _G_python_1086, lastError = eval(self._G_expr_1085, self.globals, _locals), None
            self.considerError(lastError, 'IdInColl')
            return (_G_python_1086, self.currentError)


        def rule_FunctionInvocation(self):
            _locals = {'self': self}
            self.locals['FunctionInvocation'] = _locals
            self._trace(' -> ["Single"', (8725, 8738), self.input.position)
            _G_apply_1087, lastError = self._apply(self.rule_FunctionName, "FunctionName", [])
            self.considerError(lastError, 'FunctionInvocation')
            _locals['func'] = _G_apply_1087
            self._trace(']\n         | Relationsh', (8743, 8766), self.input.position)
            _G_apply_1088, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'FunctionInvocation')
            self._trace('ipsP', (8766, 8770), self.input.position)
            _G_exactly_1089, lastError = self.exactly('(')
            self.considerError(lastError, 'FunctionInvocation')
            self._trace('att', (8770, 8773), self.input.position)
            _G_apply_1090, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'FunctionInvocation')
            def _G_optional_1091():
                self._trace('l', (8795, 8796), self.input.position)
                _G_apply_1092, lastError = self._apply(self.rule_D, "D", [])
                self.considerError(lastError, None)
                self._trace('at', (8796, 8798), self.input.position)
                _G_apply_1093, lastError = self._apply(self.rule_I, "I", [])
                self.considerError(lastError, None)
                self._trace('io', (8798, 8800), self.input.position)
                _G_apply_1094, lastError = self._apply(self.rule_S, "S", [])
                self.considerError(lastError, None)
                self._trace('ns', (8800, 8802), self.input.position)
                _G_apply_1095, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                self._trace('hi', (8802, 8804), self.input.position)
                _G_apply_1096, lastError = self._apply(self.rule_I, "I", [])
                self.considerError(lastError, None)
                self._trace('ps', (8804, 8806), self.input.position)
                _G_apply_1097, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace('Pa', (8806, 8808), self.input.position)
                _G_apply_1098, lastError = self._apply(self.rule_C, "C", [])
                self.considerError(lastError, None)
                self._trace('tt', (8808, 8810), self.input.position)
                _G_apply_1099, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                self._trace('ern', (8810, 8813), self.input.position)
                _G_apply_1100, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                _G_python_1101, lastError = ("distinct"), None
                self.considerError(lastError, None)
                return (_G_python_1101, self.currentError)
            def _G_optional_1102():
                return (None, self.input.nullError())
            _G_or_1103, lastError = self._or([_G_optional_1091, _G_optional_1102])
            self.considerError(lastError, 'FunctionInvocation')
            _locals['distinct'] = _G_or_1103
            def _G_or_1104():
                self._trace('FunctionInvocation\n         | Varia', (8860, 8895), self.input.position)
                _G_apply_1105, lastError = self._apply(self.rule_Expression, "Expression", [])
                self.considerError(lastError, None)
                _locals['head'] = _G_apply_1105
                def _G_many_1106():
                    self._trace("n = '(' WS Expression:ex WS ')' ", (8926, 8958), self.input.position)
                    _G_exactly_1107, lastError = self.exactly(',')
                    self.considerError(lastError, None)
                    self._trace('-> ', (8958, 8961), self.input.position)
                    _G_apply_1108, lastError = self._apply(self.rule_WS, "WS", [])
                    self.considerError(lastError, None)
                    self._trace('ex\n\n    Rel', (8961, 8972), self.input.position)
                    _G_apply_1109, lastError = self._apply(self.rule_Expression, "Expression", [])
                    self.considerError(lastError, None)
                    return (_G_apply_1109, self.currentError)
                _G_many_1110, lastError = self.many(_G_many_1106)
                self.considerError(lastError, None)
                _locals['tail'] = _G_many_1110
                _G_python_1111, lastError = eval(self._G_expr_423, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_1111, self.currentError)
            def _G_or_1112():
                _G_python_1113, lastError = ([]), None
                self.considerError(lastError, None)
                return (_G_python_1113, self.currentError)
            _G_or_1114, lastError = self._or([_G_or_1104, _G_or_1112])
            self.considerError(lastError, 'FunctionInvocation')
            _locals['args'] = _G_or_1114
            self._trace('  \n    GraphRelationshi', (9076, 9099), self.input.position)
            _G_apply_1115, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'FunctionInvocation')
            self._trace('psPa', (9099, 9103), self.input.position)
            _G_exactly_1116, lastError = self.exactly(')')
            self.considerError(lastError, 'FunctionInvocation')
            _G_python_1118, lastError = eval(self._G_expr_1117, self.globals, _locals), None
            self.considerError(lastError, 'FunctionInvocation')
            return (_G_python_1118, self.currentError)


        def rule_FunctionName(self):
            _locals = {'self': self}
            self.locals['FunctionName'] = _locals
            self._trace('rnElementChai', (9153, 9166), self.input.position)
            _G_apply_1119, lastError = self._apply(self.rule_SymbolicName, "SymbolicName", [])
            self.considerError(lastError, 'FunctionName')
            return (_G_apply_1119, self.currentError)


        def rule_ListComprehension(self):
            _locals = {'self': self}
            self.locals['ListComprehension'] = _locals
            self._trace('atio', (9187, 9191), self.input.position)
            _G_exactly_1120, lastError = self.exactly('[')
            self.considerError(lastError, 'ListComprehension')
            self._trace('nshipsPattern", v', (9191, 9208), self.input.position)
            _G_apply_1121, lastError = self._apply(self.rule_FilterExpression, "FilterExpression", [])
            self.considerError(lastError, 'ListComprehension')
            _locals['fex'] = _G_apply_1121
            def _G_optional_1122():
                self._trace('pe', (9214, 9216), self.input.position)
                _G_apply_1123, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('c]\n\n', (9216, 9220), self.input.position)
                _G_exactly_1124, lastError = self.exactly('|')
                self.considerError(lastError, None)
                self._trace('    FilterE', (9220, 9231), self.input.position)
                _G_apply_1125, lastError = self._apply(self.rule_Expression, "Expression", [])
                self.considerError(lastError, None)
                return (_G_apply_1125, self.currentError)
            def _G_optional_1126():
                return (None, self.input.nullError())
            _G_or_1127, lastError = self._or([_G_optional_1122, _G_optional_1126])
            self.considerError(lastError, 'ListComprehension')
            _locals['ex'] = _G_or_1127
            self._trace('sion', (9236, 9240), self.input.position)
            _G_exactly_1128, lastError = self.exactly(']')
            self.considerError(lastError, 'ListComprehension')
            _G_python_1130, lastError = eval(self._G_expr_1129, self.globals, _locals), None
            self.considerError(lastError, 'ListComprehension')
            return (_G_python_1130, self.currentError)


        def rule_PropertyLookup(self):
            _locals = {'self': self}
            self.locals['PropertyLookup'] = _locals
            self._trace('\n\n ', (9371, 9374), self.input.position)
            _G_apply_1131, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'PropertyLookup')
            self._trace('   F', (9374, 9378), self.input.position)
            _G_exactly_1132, lastError = self.exactly('.')
            self.considerError(lastError, 'PropertyLookup')
            self._trace('unc', (9378, 9381), self.input.position)
            _G_apply_1133, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'PropertyLookup')
            self._trace('tionInvocation =', (9381, 9397), self.input.position)
            _G_apply_1134, lastError = self._apply(self.rule_PropertyKeyName, "PropertyKeyName", [])
            self.considerError(lastError, 'PropertyLookup')
            _locals['n'] = _G_apply_1134
            _G_python_1136, lastError = eval(self._G_expr_1135, self.globals, _locals), None
            self.considerError(lastError, 'PropertyLookup')
            return (_G_python_1136, self.currentError)


        def rule_CaseExpression(self):
            _locals = {'self': self}
            self.locals['CaseExpression'] = _locals
            self._trace(" '(' WS\n           ", (9442, 9461), self.input.position)
            _G_apply_1137, lastError = self._apply(self.rule_C, "C", [])
            self.considerError(lastError, 'CaseExpression')
            self._trace('  ', (9461, 9463), self.input.position)
            _G_apply_1138, lastError = self._apply(self.rule_A, "A", [])
            self.considerError(lastError, 'CaseExpression')
            self._trace('  ', (9463, 9465), self.input.position)
            _G_apply_1139, lastError = self._apply(self.rule_S, "S", [])
            self.considerError(lastError, 'CaseExpression')
            self._trace('  ', (9465, 9467), self.input.position)
            _G_apply_1140, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'CaseExpression')
            self._trace('   ', (9467, 9470), self.input.position)
            _G_apply_1141, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'CaseExpression')
            def _G_optional_1142():
                self._trace('T WS -> "d', (9489, 9499), self.input.position)
                _G_apply_1143, lastError = self._apply(self.rule_Expression, "Expression", [])
                self.considerError(lastError, None)
                return (_G_apply_1143, self.currentError)
            def _G_optional_1144():
                return (None, self.input.nullError())
            _G_or_1145, lastError = self._or([_G_optional_1142, _G_optional_1144])
            self.considerError(lastError, 'CaseExpression')
            _locals['ex'] = _G_or_1145
            def _G_many1_1146():
                self._trace('  ', (9523, 9525), self.input.position)
                _G_apply_1147, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('                 ', (9525, 9542), self.input.position)
                _G_apply_1148, lastError = self._apply(self.rule_CaseAlternatives, "CaseAlternatives", [])
                self.considerError(lastError, None)
                return (_G_apply_1148, self.currentError)
            _G_many1_1149, lastError = self.many(_G_many1_1146, _G_many1_1146())
            self.considerError(lastError, 'CaseExpression')
            _locals['cas'] = _G_many1_1149
            def _G_optional_1150():
                self._trace('  ', (9568, 9570), self.input.position)
                _G_apply_1151, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('  ', (9570, 9572), self.input.position)
                _G_apply_1152, lastError = self._apply(self.rule_E, "E", [])
                self.considerError(lastError, None)
                self._trace(' E', (9572, 9574), self.input.position)
                _G_apply_1153, lastError = self._apply(self.rule_L, "L", [])
                self.considerError(lastError, None)
                self._trace('xp', (9574, 9576), self.input.position)
                _G_apply_1154, lastError = self._apply(self.rule_S, "S", [])
                self.considerError(lastError, None)
                self._trace('re', (9576, 9578), self.input.position)
                _G_apply_1155, lastError = self._apply(self.rule_E, "E", [])
                self.considerError(lastError, None)
                self._trace('ssi', (9578, 9581), self.input.position)
                _G_apply_1156, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('on:head\n   ', (9581, 9592), self.input.position)
                _G_apply_1157, lastError = self._apply(self.rule_Expression, "Expression", [])
                self.considerError(lastError, None)
                return (_G_apply_1157, self.currentError)
            def _G_optional_1158():
                return (None, self.input.nullError())
            _G_or_1159, lastError = self._or([_G_optional_1150, _G_optional_1158])
            self.considerError(lastError, 'CaseExpression')
            _locals['el'] = _G_or_1159
            self._trace('                    ', (9597, 9617), self.input.position)
            _G_apply_1160, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'CaseExpression')
            self._trace('(\n', (9617, 9619), self.input.position)
            _G_apply_1161, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'CaseExpression')
            self._trace('  ', (9619, 9621), self.input.position)
            _G_apply_1162, lastError = self._apply(self.rule_N, "N", [])
            self.considerError(lastError, 'CaseExpression')
            self._trace('  ', (9621, 9623), self.input.position)
            _G_apply_1163, lastError = self._apply(self.rule_D, "D", [])
            self.considerError(lastError, 'CaseExpression')
            _G_python_1165, lastError = eval(self._G_expr_1164, self.globals, _locals), None
            self.considerError(lastError, 'CaseExpression')
            return (_G_python_1165, self.currentError)


        def rule_CaseAlternatives(self):
            _locals = {'self': self}
            self.locals['CaseAlternatives'] = _locals
            self._trace('  ', (9685, 9687), self.input.position)
            _G_apply_1166, lastError = self._apply(self.rule_W, "W", [])
            self.considerError(lastError, 'CaseAlternatives')
            self._trace('  ', (9687, 9689), self.input.position)
            _G_apply_1167, lastError = self._apply(self.rule_H, "H", [])
            self.considerError(lastError, 'CaseAlternatives')
            self._trace('  ', (9689, 9691), self.input.position)
            _G_apply_1168, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'CaseAlternatives')
            self._trace('  ', (9691, 9693), self.input.position)
            _G_apply_1169, lastError = self._apply(self.rule_N, "N", [])
            self.considerError(lastError, 'CaseAlternatives')
            self._trace('   ', (9693, 9696), self.input.position)
            _G_apply_1170, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'CaseAlternatives')
            self._trace(' )*:tail ->', (9696, 9707), self.input.position)
            _G_apply_1171, lastError = self._apply(self.rule_Expression, "Expression", [])
            self.considerError(lastError, 'CaseAlternatives')
            _locals['ex1'] = _G_apply_1171
            self._trace('ad]', (9711, 9714), self.input.position)
            _G_apply_1172, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'CaseAlternatives')
            self._trace(' +', (9714, 9716), self.input.position)
            _G_apply_1173, lastError = self._apply(self.rule_T, "T", [])
            self.considerError(lastError, 'CaseAlternatives')
            self._trace(' t', (9716, 9718), self.input.position)
            _G_apply_1174, lastError = self._apply(self.rule_H, "H", [])
            self.considerError(lastError, 'CaseAlternatives')
            self._trace('ai', (9718, 9720), self.input.position)
            _G_apply_1175, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'CaseAlternatives')
            self._trace('l\n', (9720, 9722), self.input.position)
            _G_apply_1176, lastError = self._apply(self.rule_N, "N", [])
            self.considerError(lastError, 'CaseAlternatives')
            self._trace('   ', (9722, 9725), self.input.position)
            _G_apply_1177, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'CaseAlternatives')
            self._trace('           ', (9725, 9736), self.input.position)
            _G_apply_1178, lastError = self._apply(self.rule_Expression, "Expression", [])
            self.considerError(lastError, 'CaseAlternatives')
            _locals['ex2'] = _G_apply_1178
            _G_python_1180, lastError = eval(self._G_expr_1179, self.globals, _locals), None
            self.considerError(lastError, 'CaseAlternatives')
            return (_G_python_1180, self.currentError)


        def rule_Variable(self):
            _locals = {'self': self}
            self.locals['Variable'] = _locals
            self._trace('            )', (9766, 9779), self.input.position)
            _G_apply_1181, lastError = self._apply(self.rule_SymbolicName, "SymbolicName", [])
            self.considerError(lastError, 'Variable')
            _locals['s'] = _G_apply_1181
            _G_python_1183, lastError = eval(self._G_expr_1182, self.globals, _locals), None
            self.considerError(lastError, 'Variable')
            return (_G_python_1183, self.currentError)


        def rule_StringLiteral(self):
            _locals = {'self': self}
            self.locals['StringLiteral'] = _locals
            def _G_or_1184():
                self._trace('["call", func, dis', (9819, 9837), self.input.position)
                _G_exactly_1185, lastError = self.exactly('"')
                self.considerError(lastError, None)
                def _G_many_1186():
                    def _G_or_1187():
                        def _G_not_1188():
                            def _G_or_1189():
                                self._trace('t, ', (9841, 9844), self.input.position)
                                _G_exactly_1190, lastError = self.exactly('"')
                                self.considerError(lastError, None)
                                return (_G_exactly_1190, self.currentError)
                            def _G_or_1191():
                                self._trace('rgs]', (9845, 9849), self.input.position)
                                _G_exactly_1192, lastError = self.exactly('\\')
                                self.considerError(lastError, None)
                                return (_G_exactly_1192, self.currentError)
                            _G_or_1193, lastError = self._or([_G_or_1189, _G_or_1191])
                            self.considerError(lastError, None)
                            return (_G_or_1193, self.currentError)
                        _G_not_1194, lastError = self._not(_G_not_1188)
                        self.considerError(lastError, None)
                        self._trace('\n    Func', (9850, 9859), self.input.position)
                        _G_apply_1195, lastError = self._apply(self.rule_anything, "anything", [])
                        self.considerError(lastError, None)
                        return (_G_apply_1195, self.currentError)
                    def _G_or_1196():
                        self._trace('onName = Sym', (9861, 9873), self.input.position)
                        _G_apply_1197, lastError = self._apply(self.rule_EscapedChar, "EscapedChar", [])
                        self.considerError(lastError, None)
                        return (_G_apply_1197, self.currentError)
                    _G_or_1198, lastError = self._or([_G_or_1187, _G_or_1196])
                    self.considerError(lastError, None)
                    return (_G_or_1198, self.currentError)
                _G_many_1199, lastError = self.many(_G_many_1186)
                self.considerError(lastError, None)
                _locals['cs'] = _G_many_1199
                self._trace('Name', (9878, 9882), self.input.position)
                _G_exactly_1200, lastError = self.exactly('"')
                self.considerError(lastError, None)
                _G_python_1202, lastError = eval(self._G_expr_1201, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_1202, self.currentError)
            def _G_or_1203():
                self._trace('ilte', (9913, 9917), self.input.position)
                _G_apply_1204, lastError = self._apply(self.rule_token, "token", ["'"])
                self.considerError(lastError, None)
                def _G_many_1205():
                    def _G_or_1206():
                        def _G_not_1207():
                            def _G_or_1208():
                                self._trace('res', (9921, 9924), self.input.position)
                                _G_apply_1209, lastError = self._apply(self.rule_token, "token", ["'"])
                                self.considerError(lastError, None)
                                return (_G_apply_1209, self.currentError)
                            def _G_or_1210():
                                self._trace('ion:', (9925, 9929), self.input.position)
                                _G_exactly_1211, lastError = self.exactly('\\')
                                self.considerError(lastError, None)
                                return (_G_exactly_1211, self.currentError)
                            _G_or_1212, lastError = self._or([_G_or_1208, _G_or_1210])
                            self.considerError(lastError, None)
                            return (_G_or_1212, self.currentError)
                        _G_not_1213, lastError = self._not(_G_not_1207)
                        self.considerError(lastError, None)
                        self._trace("ex (WS '|", (9930, 9939), self.input.position)
                        _G_apply_1214, lastError = self._apply(self.rule_anything, "anything", [])
                        self.considerError(lastError, None)
                        return (_G_apply_1214, self.currentError)
                    def _G_or_1215():
                        self._trace('Expression)?', (9941, 9953), self.input.position)
                        _G_apply_1216, lastError = self._apply(self.rule_EscapedChar, "EscapedChar", [])
                        self.considerError(lastError, None)
                        return (_G_apply_1216, self.currentError)
                    _G_or_1217, lastError = self._or([_G_or_1206, _G_or_1215])
                    self.considerError(lastError, None)
                    return (_G_or_1217, self.currentError)
                _G_many_1218, lastError = self.many(_G_many_1205)
                self.considerError(lastError, None)
                _locals['cs'] = _G_many_1218
                self._trace("]' -", (9958, 9962), self.input.position)
                _G_apply_1219, lastError = self._apply(self.rule_token, "token", ["'"])
                self.considerError(lastError, None)
                _G_python_1220, lastError = eval(self._G_expr_1201, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_1220, self.currentError)
            _G_or_1221, lastError = self._or([_G_or_1184, _G_or_1203])
            self.considerError(lastError, 'StringLiteral')
            _locals['l'] = _G_or_1221
            _G_python_1223, lastError = eval(self._G_expr_1222, self.globals, _locals), None
            self.considerError(lastError, 'StringLiteral')
            return (_G_python_1223, self.currentError)


        def rule_EscapedChar(self):
            _locals = {'self': self}
            self.locals['EscapedChar'] = _locals
            self._trace(' ((Pr', (10028, 10033), self.input.position)
            _G_exactly_1224, lastError = self.exactly('\\')
            self.considerError(lastError, 'EscapedChar')
            def _G_or_1225():
                self._trace("('?'", (10047, 10051), self.input.position)
                _G_exactly_1226, lastError = self.exactly('\\')
                self.considerError(lastError, None)
                _G_python_1227, lastError = ('\\'), None
                self.considerError(lastError, None)
                return (_G_python_1227, self.currentError)
            def _G_or_1228():
                self._trace('Name', (10073, 10077), self.input.position)
                _G_apply_1229, lastError = self._apply(self.rule_token, "token", ["'"])
                self.considerError(lastError, None)
                _G_python_1230, lastError = ("'"), None
                self.considerError(lastError, None)
                return (_G_python_1230, self.currentError)
            def _G_or_1231():
                self._trace('= WS', (10098, 10102), self.input.position)
                _G_exactly_1232, lastError = self.exactly('"')
                self.considerError(lastError, None)
                _G_python_1233, lastError = ('"'), None
                self.considerError(lastError, None)
                return (_G_python_1233, self.currentError)
            def _G_or_1234():
                self._trace('me', (10123, 10125), self.input.position)
                _G_apply_1235, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                _G_python_1236, lastError = ('\n'), None
                self.considerError(lastError, None)
                return (_G_python_1236, self.currentError)
            def _G_or_1237():
                self._trace('",', (10147, 10149), self.input.position)
                _G_apply_1238, lastError = self._apply(self.rule_R, "R", [])
                self.considerError(lastError, None)
                _G_python_1239, lastError = ('\r'), None
                self.considerError(lastError, None)
                return (_G_python_1239, self.currentError)
            def _G_or_1240():
                self._trace('n ', (10171, 10173), self.input.position)
                _G_apply_1241, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                _G_python_1242, lastError = ('\t'), None
                self.considerError(lastError, None)
                return (_G_python_1242, self.currentError)
            def _G_or_1243():
                self._trace(' C A', (10195, 10199), self.input.position)
                _G_exactly_1244, lastError = self.exactly('_')
                self.considerError(lastError, None)
                _G_python_1245, lastError = ('_'), None
                self.considerError(lastError, None)
                return (_G_python_1245, self.currentError)
            def _G_or_1246():
                self._trace('    ', (10220, 10224), self.input.position)
                _G_exactly_1247, lastError = self.exactly('%')
                self.considerError(lastError, None)
                _G_python_1248, lastError = ('%'), None
                self.considerError(lastError, None)
                return (_G_python_1248, self.currentError)
            _G_or_1249, lastError = self._or([_G_or_1225, _G_or_1228, _G_or_1231, _G_or_1234, _G_or_1237, _G_or_1240, _G_or_1243, _G_or_1246])
            self.considerError(lastError, 'EscapedChar')
            return (_G_or_1249, self.currentError)


        def rule_NumberLiteral(self):
            _locals = {'self': self}
            self.locals['NumberLiteral'] = _locals
            def _G_or_1250():
                self._trace('  (WS CaseAlternatives)+:cas', (10264, 10292), self.input.position)
                _G_apply_1251, lastError = self._apply(self.rule_DoubleLiteral, "DoubleLiteral", [])
                self.considerError(lastError, None)
                return (_G_apply_1251, self.currentError)
            def _G_or_1252():
                self._trace('       (WS E L ', (10308, 10323), self.input.position)
                _G_apply_1253, lastError = self._apply(self.rule_IntegerLiteral, "IntegerLiteral", [])
                self.considerError(lastError, None)
                return (_G_apply_1253, self.currentError)
            _G_or_1254, lastError = self._or([_G_or_1250, _G_or_1252])
            self.considerError(lastError, 'NumberLiteral')
            _locals['l'] = _G_or_1254
            _G_python_1255, lastError = eval(self._G_expr_1222, self.globals, _locals), None
            self.considerError(lastError, 'NumberLiteral')
            return (_G_python_1255, self.currentError)


        def rule_MapLiteral(self):
            _locals = {'self': self}
            self.locals['MapLiteral'] = _locals
            self._trace(' D\n ', (10373, 10377), self.input.position)
            _G_exactly_1256, lastError = self.exactly('{')
            self.considerError(lastError, 'MapLiteral')
            self._trace('   ', (10377, 10380), self.input.position)
            _G_apply_1257, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'MapLiteral')
            def _G_or_1258():
                self._trace('cas, el]\n\n    CaseAlternatives = W H', (10413, 10449), self.input.position)
                _G_apply_1259, lastError = self._apply(self.rule_PropertyKeyName, "PropertyKeyName", [])
                self.considerError(lastError, None)
                _locals['k'] = _G_apply_1259
                self._trace(' N ', (10451, 10454), self.input.position)
                _G_apply_1260, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('WS E', (10454, 10458), self.input.position)
                _G_exactly_1261, lastError = self.exactly(':')
                self.considerError(lastError, None)
                self._trace('xpr', (10458, 10461), self.input.position)
                _G_apply_1262, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('ession:ex1 ', (10461, 10472), self.input.position)
                _G_apply_1263, lastError = self._apply(self.rule_Expression, "Expression", [])
                self.considerError(lastError, None)
                _locals['v'] = _G_apply_1263
                _G_python_1265, lastError = eval(self._G_expr_1264, self.globals, _locals), None
                self.considerError(lastError, None)
                _locals['head'] = _G_python_1265
                self._trace('1, ', (10507, 10510), self.input.position)
                _G_apply_1266, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                def _G_many_1267():
                    self._trace(' = SymbolicName:s -> ["V', (10528, 10552), self.input.position)
                    _G_exactly_1268, lastError = self.exactly(',')
                    self.considerError(lastError, None)
                    self._trace('ari', (10552, 10555), self.input.position)
                    _G_apply_1269, lastError = self._apply(self.rule_WS, "WS", [])
                    self.considerError(lastError, None)
                    self._trace('able", s]\n\n    S', (10555, 10571), self.input.position)
                    _G_apply_1270, lastError = self._apply(self.rule_PropertyKeyName, "PropertyKeyName", [])
                    self.considerError(lastError, None)
                    _locals['k'] = _G_apply_1270
                    self._trace('ing', (10573, 10576), self.input.position)
                    _G_apply_1271, lastError = self._apply(self.rule_WS, "WS", [])
                    self.considerError(lastError, None)
                    self._trace('Lite', (10576, 10580), self.input.position)
                    _G_exactly_1272, lastError = self.exactly(':')
                    self.considerError(lastError, None)
                    self._trace('ral', (10580, 10583), self.input.position)
                    _G_apply_1273, lastError = self._apply(self.rule_WS, "WS", [])
                    self.considerError(lastError, None)
                    self._trace(' = (\n      ', (10583, 10594), self.input.position)
                    _G_apply_1274, lastError = self._apply(self.rule_Expression, "Expression", [])
                    self.considerError(lastError, None)
                    _locals['v'] = _G_apply_1274
                    self._trace('   ', (10596, 10599), self.input.position)
                    _G_apply_1275, lastError = self._apply(self.rule_WS, "WS", [])
                    self.considerError(lastError, None)
                    _G_python_1276, lastError = eval(self._G_expr_1264, self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_1276, self.currentError)
                _G_many_1277, lastError = self.many(_G_many_1267)
                self.considerError(lastError, None)
                _locals['tail'] = _G_many_1277
                _G_python_1278, lastError = eval(self._G_expr_423, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_1278, self.currentError)
            def _G_or_1279():
                _G_python_1280, lastError = ([]), None
                self.considerError(lastError, None)
                return (_G_python_1280, self.currentError)
            _G_or_1281, lastError = self._or([_G_or_1258, _G_or_1279])
            self.considerError(lastError, 'MapLiteral')
            _locals['pairs'] = _G_or_1281
            self._trace('          | "\'" ', (10678, 10694), self.input.position)
            _G_exactly_1282, lastError = self.exactly('}')
            self.considerError(lastError, 'MapLiteral')
            _G_python_1284, lastError = eval(self._G_expr_1283, self.globals, _locals), None
            self.considerError(lastError, 'MapLiteral')
            return (_G_python_1284, self.currentError)


        def rule_Parameter(self):
            _locals = {'self': self}
            self.locals['Parameter'] = _locals
            self._trace('"\'" ', (10735, 10739), self.input.position)
            _G_exactly_1285, lastError = self.exactly('{')
            self.considerError(lastError, 'Parameter')
            self._trace('-> ', (10739, 10742), self.input.position)
            _G_apply_1286, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'Parameter')
            def _G_or_1287():
                self._trace('.join(cs)\n  ', (10744, 10756), self.input.position)
                _G_apply_1288, lastError = self._apply(self.rule_SymbolicName, "SymbolicName", [])
                self.considerError(lastError, None)
                return (_G_apply_1288, self.currentError)
            def _G_or_1289():
                self._trace('              )', (10758, 10773), self.input.position)
                _G_apply_1290, lastError = self._apply(self.rule_DecimalInteger, "DecimalInteger", [])
                self.considerError(lastError, None)
                return (_G_apply_1290, self.currentError)
            _G_or_1291, lastError = self._or([_G_or_1287, _G_or_1289])
            self.considerError(lastError, 'Parameter')
            _locals['p'] = _G_or_1291
            self._trace('-> ', (10776, 10779), self.input.position)
            _G_apply_1292, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'Parameter')
            self._trace('["Li', (10779, 10783), self.input.position)
            _G_exactly_1293, lastError = self.exactly('}')
            self.considerError(lastError, 'Parameter')
            _G_python_1295, lastError = eval(self._G_expr_1294, self.globals, _locals), None
            self.considerError(lastError, 'Parameter')
            return (_G_python_1295, self.currentError)


        def rule_PropertyExpression(self):
            _locals = {'self': self}
            self.locals['PropertyExpression'] = _locals
            self._trace('     ', (10825, 10830), self.input.position)
            _G_apply_1296, lastError = self._apply(self.rule_Atom, "Atom", [])
            self.considerError(lastError, 'PropertyExpression')
            _locals['a'] = _G_apply_1296
            def _G_many_1297():
                self._trace("('", (10834, 10836), self.input.position)
                _G_apply_1298, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace("\\\\' -> '\\\\'\n   ", (10836, 10851), self.input.position)
                _G_apply_1299, lastError = self._apply(self.rule_PropertyLookup, "PropertyLookup", [])
                self.considerError(lastError, None)
                return (_G_apply_1299, self.currentError)
            _G_many_1300, lastError = self.many(_G_many_1297)
            self.considerError(lastError, 'PropertyExpression')
            _locals['opts'] = _G_many_1300
            _G_python_1302, lastError = eval(self._G_expr_1301, self.globals, _locals), None
            self.considerError(lastError, 'PropertyExpression')
            return (_G_python_1302, self.currentError)


        def rule_PropertyKeyName(self):
            _locals = {'self': self}
            self.locals['PropertyKeyName'] = _locals
            self._trace("'\n           ", (10904, 10917), self.input.position)
            _G_apply_1303, lastError = self._apply(self.rule_SymbolicName, "SymbolicName", [])
            self.considerError(lastError, 'PropertyKeyName')
            return (_G_apply_1303, self.currentError)


        def rule_IntegerLiteral(self):
            _locals = {'self': self}
            self.locals['IntegerLiteral'] = _locals
            def _G_or_1304():
                self._trace('           ', (10935, 10946), self.input.position)
                _G_apply_1305, lastError = self._apply(self.rule_HexInteger, "HexInteger", [])
                self.considerError(lastError, None)
                return (_G_apply_1305, self.currentError)
            def _G_or_1306():
                self._trace('             ', (10963, 10976), self.input.position)
                _G_apply_1307, lastError = self._apply(self.rule_OctalInteger, "OctalInteger", [])
                self.considerError(lastError, None)
                return (_G_apply_1307, self.currentError)
            def _G_or_1308():
                self._trace('             | ', (10993, 11008), self.input.position)
                _G_apply_1309, lastError = self._apply(self.rule_DecimalInteger, "DecimalInteger", [])
                self.considerError(lastError, None)
                return (_G_apply_1309, self.currentError)
            _G_or_1310, lastError = self._or([_G_or_1304, _G_or_1306, _G_or_1308])
            self.considerError(lastError, 'IntegerLiteral')
            return (_G_or_1310, self.currentError)


        def rule_OctalDigit(self):
            _locals = {'self': self}
            self.locals['OctalDigit'] = _locals
            def _G_not_1311():
                def _G_or_1312():
                    self._trace('   ', (11025, 11028), self.input.position)
                    _G_exactly_1313, lastError = self.exactly('8')
                    self.considerError(lastError, None)
                    return (_G_exactly_1313, self.currentError)
                def _G_or_1314():
                    self._trace('   ', (11029, 11032), self.input.position)
                    _G_exactly_1315, lastError = self.exactly('9')
                    self.considerError(lastError, None)
                    return (_G_exactly_1315, self.currentError)
                _G_or_1316, lastError = self._or([_G_or_1312, _G_or_1314])
                self.considerError(lastError, None)
                return (_G_or_1316, self.currentError)
            _G_not_1317, lastError = self._not(_G_not_1311)
            self.considerError(lastError, 'OctalDigit')
            self._trace("  | '%", (11033, 11039), self.input.position)
            _G_apply_1318, lastError = self._apply(self.rule_digit, "digit", [])
            self.considerError(lastError, 'OctalDigit')
            return (_G_apply_1318, self.currentError)


        def rule_OctalInteger(self):
            _locals = {'self': self}
            self.locals['OctalInteger'] = _locals
            self._trace('    ', (11055, 11059), self.input.position)
            _G_exactly_1319, lastError = self.exactly('0')
            self.considerError(lastError, 'OctalInteger')
            def _G_consumedby_1320():
                def _G_many1_1321():
                    self._trace('   )\n\n    ', (11061, 11071), self.input.position)
                    _G_apply_1322, lastError = self._apply(self.rule_OctalDigit, "OctalDigit", [])
                    self.considerError(lastError, None)
                    return (_G_apply_1322, self.currentError)
                _G_many1_1323, lastError = self.many(_G_many1_1321, _G_many1_1321())
                self.considerError(lastError, None)
                return (_G_many1_1323, self.currentError)
            _G_consumedby_1324, lastError = self.consumedby(_G_consumedby_1320)
            self.considerError(lastError, 'OctalInteger')
            _locals['ds'] = _G_consumedby_1324
            _G_python_1326, lastError = eval(self._G_expr_1325, self.globals, _locals), None
            self.considerError(lastError, 'OctalInteger')
            return (_G_python_1326, self.currentError)


        def rule_HexDigit(self):
            _locals = {'self': self}
            self.locals['HexDigit'] = _locals
            def _G_or_1327():
                self._trace('     D', (11102, 11108), self.input.position)
                _G_apply_1328, lastError = self._apply(self.rule_digit, "digit", [])
                self.considerError(lastError, None)
                return (_G_apply_1328, self.currentError)
            def _G_or_1329():
                self._trace('bl', (11110, 11112), self.input.position)
                _G_apply_1330, lastError = self._apply(self.rule_A, "A", [])
                self.considerError(lastError, None)
                return (_G_apply_1330, self.currentError)
            def _G_or_1331():
                self._trace('it', (11114, 11116), self.input.position)
                _G_apply_1332, lastError = self._apply(self.rule_B, "B", [])
                self.considerError(lastError, None)
                return (_G_apply_1332, self.currentError)
            def _G_or_1333():
                self._trace('al', (11118, 11120), self.input.position)
                _G_apply_1334, lastError = self._apply(self.rule_C, "C", [])
                self.considerError(lastError, None)
                return (_G_apply_1334, self.currentError)
            def _G_or_1335():
                self._trace('  ', (11122, 11124), self.input.position)
                _G_apply_1336, lastError = self._apply(self.rule_D, "D", [])
                self.considerError(lastError, None)
                return (_G_apply_1336, self.currentError)
            def _G_or_1337():
                self._trace('  ', (11126, 11128), self.input.position)
                _G_apply_1338, lastError = self._apply(self.rule_E, "E", [])
                self.considerError(lastError, None)
                return (_G_apply_1338, self.currentError)
            def _G_or_1339():
                self._trace('  ', (11130, 11132), self.input.position)
                _G_apply_1340, lastError = self._apply(self.rule_F, "F", [])
                self.considerError(lastError, None)
                return (_G_apply_1340, self.currentError)
            _G_or_1341, lastError = self._or([_G_or_1327, _G_or_1329, _G_or_1331, _G_or_1333, _G_or_1335, _G_or_1337, _G_or_1339])
            self.considerError(lastError, 'HexDigit')
            return (_G_or_1341, self.currentError)


        def rule_HexInteger(self):
            _locals = {'self': self}
            self.locals['HexInteger'] = _locals
            self._trace('erLi', (11146, 11150), self.input.position)
            _G_exactly_1342, lastError = self.exactly('0')
            self.considerError(lastError, 'HexInteger')
            self._trace('te', (11150, 11152), self.input.position)
            _G_apply_1343, lastError = self._apply(self.rule_X, "X", [])
            self.considerError(lastError, 'HexInteger')
            def _G_consumedby_1344():
                def _G_many1_1345():
                    self._trace('l\n      ', (11154, 11162), self.input.position)
                    _G_apply_1346, lastError = self._apply(self.rule_HexDigit, "HexDigit", [])
                    self.considerError(lastError, None)
                    return (_G_apply_1346, self.currentError)
                _G_many1_1347, lastError = self.many(_G_many1_1345, _G_many1_1345())
                self.considerError(lastError, None)
                return (_G_many1_1347, self.currentError)
            _G_consumedby_1348, lastError = self.consumedby(_G_consumedby_1344)
            self.considerError(lastError, 'HexInteger')
            _locals['ds'] = _G_consumedby_1348
            _G_python_1350, lastError = eval(self._G_expr_1349, self.globals, _locals), None
            self.considerError(lastError, 'HexInteger')
            return (_G_python_1350, self.currentError)


        def rule_DecimalInteger(self):
            _locals = {'self': self}
            self.locals['DecimalInteger'] = _locals
            def _G_consumedby_1351():
                def _G_many1_1352():
                    self._trace('apLit', (11202, 11207), self.input.position)
                    _G_apply_1353, lastError = self._apply(self.rule_digit, "digit", [])
                    self.considerError(lastError, None)
                    return (_G_apply_1353, self.currentError)
                _G_many1_1354, lastError = self.many(_G_many1_1352, _G_many1_1352())
                self.considerError(lastError, None)
                return (_G_many1_1354, self.currentError)
            _G_consumedby_1355, lastError = self.consumedby(_G_consumedby_1351)
            self.considerError(lastError, 'DecimalInteger')
            _locals['ds'] = _G_consumedby_1355
            _G_python_1357, lastError = eval(self._G_expr_1356, self.globals, _locals), None
            self.considerError(lastError, 'DecimalInteger')
            return (_G_python_1357, self.currentError)


        def rule_DoubleLiteral(self):
            _locals = {'self': self}
            self.locals['DoubleLiteral'] = _locals
            def _G_or_1358():
                self._trace('                    ', (11240, 11260), self.input.position)
                _G_apply_1359, lastError = self._apply(self.rule_ExponentDecimalReal, "ExponentDecimalReal", [])
                self.considerError(lastError, None)
                return (_G_apply_1359, self.currentError)
            def _G_or_1360():
                self._trace('          PropertyK', (11276, 11295), self.input.position)
                _G_apply_1361, lastError = self._apply(self.rule_RegularDecimalReal, "RegularDecimalReal", [])
                self.considerError(lastError, None)
                return (_G_apply_1361, self.currentError)
            _G_or_1362, lastError = self._or([_G_or_1358, _G_or_1360])
            self.considerError(lastError, 'DoubleLiteral')
            return (_G_or_1362, self.currentError)


        def rule_ExponentDecimalReal(self):
            _locals = {'self': self}
            self.locals['ExponentDecimalReal'] = _locals
            def _G_consumedby_1363():
                def _G_or_1364():
                    self._trace('ion:v -> (k, v', (11321, 11335), self.input.position)
                    _G_apply_1365, lastError = self._apply(self.rule_DecimalInteger, "DecimalInteger", [])
                    self.considerError(lastError, None)
                    return (_G_apply_1365, self.currentError)
                def _G_or_1366():
                    self._trace('                   ', (11337, 11356), self.input.position)
                    _G_apply_1367, lastError = self._apply(self.rule_RegularDecimalReal, "RegularDecimalReal", [])
                    self.considerError(lastError, None)
                    return (_G_apply_1367, self.currentError)
                _G_or_1368, lastError = self._or([_G_or_1364, _G_or_1366])
                self.considerError(lastError, None)
                self._trace('):', (11357, 11359), self.input.position)
                _G_apply_1369, lastError = self._apply(self.rule_E, "E", [])
                self.considerError(lastError, None)
                self._trace('head WS\n       ', (11359, 11374), self.input.position)
                _G_apply_1370, lastError = self._apply(self.rule_DecimalInteger, "DecimalInteger", [])
                self.considerError(lastError, None)
                return (_G_apply_1370, self.currentError)
            _G_consumedby_1371, lastError = self.consumedby(_G_consumedby_1363)
            self.considerError(lastError, 'ExponentDecimalReal')
            _locals['ds'] = _G_consumedby_1371
            _G_python_1373, lastError = eval(self._G_expr_1372, self.globals, _locals), None
            self.considerError(lastError, 'ExponentDecimalReal')
            return (_G_python_1373, self.currentError)


        def rule_RegularDecimalReal(self):
            _locals = {'self': self}
            self.locals['RegularDecimalReal'] = _locals
            def _G_consumedby_1374():
                def _G_many1_1375():
                    self._trace("' WS ", (11415, 11420), self.input.position)
                    _G_apply_1376, lastError = self._apply(self.rule_digit, "digit", [])
                    self.considerError(lastError, None)
                    return (_G_apply_1376, self.currentError)
                _G_many1_1377, lastError = self.many(_G_many1_1375, _G_many1_1375())
                self.considerError(lastError, None)
                self._trace('rope', (11421, 11425), self.input.position)
                _G_exactly_1378, lastError = self.exactly('.')
                self.considerError(lastError, None)
                def _G_many1_1379():
                    self._trace('rtyKey', (11425, 11431), self.input.position)
                    _G_apply_1380, lastError = self._apply(self.rule_digit, "digit", [])
                    self.considerError(lastError, None)
                    return (_G_apply_1380, self.currentError)
                _G_many1_1381, lastError = self.many(_G_many1_1379, _G_many1_1379())
                self.considerError(lastError, None)
                return (_G_many1_1381, self.currentError)
            _G_consumedby_1382, lastError = self.consumedby(_G_consumedby_1374)
            self.considerError(lastError, 'RegularDecimalReal')
            _locals['ds'] = _G_consumedby_1382
            _G_python_1383, lastError = eval(self._G_expr_1372, self.globals, _locals), None
            self.considerError(lastError, 'RegularDecimalReal')
            return (_G_python_1383, self.currentError)


        def rule_SymbolicName(self):
            _locals = {'self': self}
            self.locals['SymbolicName'] = _locals
            def _G_or_1384():
                self._trace('> (k, v)\n             ', (11465, 11487), self.input.position)
                _G_apply_1385, lastError = self._apply(self.rule_UnescapedSymbolicName, "UnescapedSymbolicName", [])
                self.considerError(lastError, None)
                return (_G_apply_1385, self.currentError)
            def _G_or_1386():
                self._trace('-> [head] + tail\n   ', (11502, 11522), self.input.position)
                _G_apply_1387, lastError = self._apply(self.rule_EscapedSymbolicName, "EscapedSymbolicName", [])
                self.considerError(lastError, None)
                return (_G_apply_1387, self.currentError)
            _G_or_1388, lastError = self._or([_G_or_1384, _G_or_1386])
            self.considerError(lastError, 'SymbolicName')
            return (_G_or_1388, self.currentError)


        def rule_UnescapedSymbolicName(self):
            _locals = {'self': self}
            self.locals['UnescapedSymbolicName'] = _locals
            def _G_consumedby_1389():
                self._trace('s\n    ', (11549, 11555), self.input.position)
                _G_apply_1390, lastError = self._apply(self.rule_letter, "letter", [])
                self.considerError(lastError, None)
                def _G_many_1391():
                    def _G_or_1392():
                        self._trace('   ', (11557, 11560), self.input.position)
                        _G_exactly_1393, lastError = self.exactly('_')
                        self.considerError(lastError, None)
                        return (_G_exactly_1393, self.currentError)
                    def _G_or_1394():
                        self._trace('     \'}\' -> ["', (11562, 11576), self.input.position)
                        _G_apply_1395, lastError = self._apply(self.rule_letterOrDigit, "letterOrDigit", [])
                        self.considerError(lastError, None)
                        return (_G_apply_1395, self.currentError)
                    _G_or_1396, lastError = self._or([_G_or_1392, _G_or_1394])
                    self.considerError(lastError, None)
                    return (_G_or_1396, self.currentError)
                _G_many_1397, lastError = self.many(_G_many_1391)
                self.considerError(lastError, None)
                return (_G_many_1397, self.currentError)
            _G_consumedby_1398, lastError = self.consumedby(_G_consumedby_1389)
            self.considerError(lastError, 'UnescapedSymbolicName')
            return (_G_consumedby_1398, self.currentError)


        def rule_EscapedSymbolicName(self):
            _locals = {'self': self}
            self.locals['EscapedSymbolicName'] = _locals
            self._trace('  Pa', (11602, 11606), self.input.position)
            _G_exactly_1399, lastError = self.exactly('`')
            self.considerError(lastError, 'EscapedSymbolicName')
            def _G_many_1400():
                def _G_or_1401():
                    def _G_not_1402():
                        self._trace('ete', (11609, 11612), self.input.position)
                        _G_exactly_1403, lastError = self.exactly('`')
                        self.considerError(lastError, None)
                        return (_G_exactly_1403, self.currentError)
                    _G_not_1404, lastError = self._not(_G_not_1402)
                    self.considerError(lastError, None)
                    self._trace("r = '{' W", (11612, 11621), self.input.position)
                    _G_apply_1405, lastError = self._apply(self.rule_anything, "anything", [])
                    self.considerError(lastError, None)
                    return (_G_apply_1405, self.currentError)
                def _G_or_1406():
                    self._trace('(Symb', (11623, 11628), self.input.position)
                    _G_apply_1407, lastError = self._apply(self.rule_token, "token", ["``"])
                    self.considerError(lastError, None)
                    _G_python_1408, lastError = ('`'), None
                    self.considerError(lastError, None)
                    return (_G_python_1408, self.currentError)
                _G_or_1409, lastError = self._or([_G_or_1401, _G_or_1406])
                self.considerError(lastError, None)
                return (_G_or_1409, self.currentError)
            _G_many_1410, lastError = self.many(_G_many_1400)
            self.considerError(lastError, 'EscapedSymbolicName')
            _locals['cs'] = _G_many_1410
            self._trace('ecim', (11640, 11644), self.input.position)
            _G_exactly_1411, lastError = self.exactly('`')
            self.considerError(lastError, 'EscapedSymbolicName')
            _G_python_1412, lastError = eval(self._G_expr_1201, self.globals, _locals), None
            self.considerError(lastError, 'EscapedSymbolicName')
            return (_G_python_1412, self.currentError)


        def rule_WS(self):
            _locals = {'self': self}
            self.locals['WS'] = _locals
            def _G_many_1413():
                self._trace('> ["Paramet', (11665, 11676), self.input.position)
                _G_apply_1414, lastError = self._apply(self.rule_whitespace, "whitespace", [])
                self.considerError(lastError, None)
                return (_G_apply_1414, self.currentError)
            _G_many_1415, lastError = self.many(_G_many_1413)
            self.considerError(lastError, 'WS')
            return (_G_many_1415, self.currentError)


        def rule_SP(self):
            _locals = {'self': self}
            self.locals['SP'] = _locals
            def _G_many1_1416():
                self._trace('\n\n    Prope', (11683, 11694), self.input.position)
                _G_apply_1417, lastError = self._apply(self.rule_whitespace, "whitespace", [])
                self.considerError(lastError, None)
                return (_G_apply_1417, self.currentError)
            _G_many1_1418, lastError = self.many(_G_many1_1416, _G_many1_1416())
            self.considerError(lastError, 'SP')
            return (_G_many1_1418, self.currentError)


        def rule_whitespace(self):
            _locals = {'self': self}
            self.locals['whitespace'] = _locals
            def _G_or_1419():
                self._trace(' Ato', (11709, 11713), self.input.position)
                _G_exactly_1420, lastError = self.exactly(' ')
                self.considerError(lastError, None)
                return (_G_exactly_1420, self.currentError)
            def _G_or_1421():
                self._trace('rtyLo', (11726, 11731), self.input.position)
                _G_exactly_1422, lastError = self.exactly('\t')
                self.considerError(lastError, None)
                return (_G_exactly_1422, self.currentError)
            def _G_or_1423():
                self._trace('> ["E', (11744, 11749), self.input.position)
                _G_exactly_1424, lastError = self.exactly('\n')
                self.considerError(lastError, None)
                return (_G_exactly_1424, self.currentError)
            def _G_or_1425():
                self._trace(', opts]\n', (11762, 11770), self.input.position)
                _G_apply_1426, lastError = self._apply(self.rule_Comment, "Comment", [])
                self.considerError(lastError, None)
                return (_G_apply_1426, self.currentError)
            _G_or_1427, lastError = self._or([_G_or_1419, _G_or_1421, _G_or_1423, _G_or_1425])
            self.considerError(lastError, 'whitespace')
            return (_G_or_1427, self.currentError)


        def rule_Comment(self):
            _locals = {'self': self}
            self.locals['Comment'] = _locals
            def _G_or_1428():
                self._trace('tyKey', (11781, 11786), self.input.position)
                _G_apply_1429, lastError = self._apply(self.rule_token, "token", ["/*"])
                self.considerError(lastError, None)
                def _G_many_1430():
                    def _G_not_1431():
                        self._trace('e = ', (11789, 11793), self.input.position)
                        _G_apply_1432, lastError = self._apply(self.rule_token, "token", ["*/"])
                        self.considerError(lastError, None)
                        return (_G_apply_1432, self.currentError)
                    _G_not_1433, lastError = self._not(_G_not_1431)
                    self.considerError(lastError, None)
                    self._trace('SymbolicN', (11793, 11802), self.input.position)
                    _G_apply_1434, lastError = self._apply(self.rule_anything, "anything", [])
                    self.considerError(lastError, None)
                    return (_G_apply_1434, self.currentError)
                _G_many_1435, lastError = self.many(_G_many_1430)
                self.considerError(lastError, None)
                self._trace('e\n\n  ', (11804, 11809), self.input.position)
                _G_apply_1436, lastError = self._apply(self.rule_token, "token", ["*/"])
                self.considerError(lastError, None)
                return (_G_apply_1436, self.currentError)
            def _G_or_1437():
                self._trace('itera', (11819, 11824), self.input.position)
                _G_apply_1438, lastError = self._apply(self.rule_token, "token", ["//"])
                self.considerError(lastError, None)
                def _G_many_1439():
                    def _G_not_1440():
                        def _G_or_1441():
                            self._trace('HexI', (11828, 11832), self.input.position)
                            _G_exactly_1442, lastError = self.exactly('\r')
                            self.considerError(lastError, None)
                            return (_G_exactly_1442, self.currentError)
                        def _G_or_1443():
                            self._trace('tege', (11833, 11837), self.input.position)
                            _G_exactly_1444, lastError = self.exactly('\n')
                            self.considerError(lastError, None)
                            return (_G_exactly_1444, self.currentError)
                        _G_or_1445, lastError = self._or([_G_or_1441, _G_or_1443])
                        self.considerError(lastError, None)
                        return (_G_or_1445, self.currentError)
                    _G_not_1446, lastError = self._not(_G_not_1440)
                    self.considerError(lastError, None)
                    self._trace('\n        ', (11838, 11847), self.input.position)
                    _G_apply_1447, lastError = self._apply(self.rule_anything, "anything", [])
                    self.considerError(lastError, None)
                    return (_G_apply_1447, self.currentError)
                _G_many_1448, lastError = self.many(_G_many_1439)
                self.considerError(lastError, None)
                def _G_optional_1449():
                    self._trace('     ', (11849, 11854), self.input.position)
                    _G_exactly_1450, lastError = self.exactly('\r')
                    self.considerError(lastError, None)
                    return (_G_exactly_1450, self.currentError)
                def _G_optional_1451():
                    return (None, self.input.nullError())
                _G_or_1452, lastError = self._or([_G_optional_1449, _G_optional_1451])
                self.considerError(lastError, None)
                def _G_or_1453():
                    self._trace(' | O', (11857, 11861), self.input.position)
                    _G_exactly_1454, lastError = self.exactly('\n')
                    self.considerError(lastError, None)
                    return (_G_exactly_1454, self.currentError)
                def _G_or_1455():
                    self._trace('tal', (11862, 11865), self.input.position)
                    _G_apply_1456, lastError = self._apply(self.rule_end, "end", [])
                    self.considerError(lastError, None)
                    return (_G_apply_1456, self.currentError)
                _G_or_1457, lastError = self._or([_G_or_1453, _G_or_1455])
                self.considerError(lastError, None)
                return (_G_or_1457, self.currentError)
            _G_or_1458, lastError = self._or([_G_or_1428, _G_or_1437])
            self.considerError(lastError, 'Comment')
            return (_G_or_1458, self.currentError)


        def rule_LeftArrowHead(self):
            _locals = {'self': self}
            self.locals['LeftArrowHead'] = _locals
            self._trace('    ', (11883, 11887), self.input.position)
            _G_exactly_1459, lastError = self.exactly('<')
            self.considerError(lastError, 'LeftArrowHead')
            return (_G_exactly_1459, self.currentError)


        def rule_RightArrowHead(self):
            _locals = {'self': self}
            self.locals['RightArrowHead'] = _locals
            self._trace('ger\n', (11905, 11909), self.input.position)
            _G_exactly_1460, lastError = self.exactly('>')
            self.considerError(lastError, 'RightArrowHead')
            return (_G_exactly_1460, self.currentError)


        def rule_Dash(self):
            _locals = {'self': self}
            self.locals['Dash'] = _locals
            self._trace('alDi', (11917, 11921), self.input.position)
            _G_exactly_1461, lastError = self.exactly('-')
            self.considerError(lastError, 'Dash')
            return (_G_exactly_1461, self.currentError)


        def rule_A(self):
            _locals = {'self': self}
            self.locals['A'] = _locals
            def _G_or_1462():
                self._trace(" ~('", (11926, 11930), self.input.position)
                _G_exactly_1463, lastError = self.exactly('A')
                self.considerError(lastError, None)
                return (_G_exactly_1463, self.currentError)
            def _G_or_1464():
                self._trace("|'9'", (11932, 11936), self.input.position)
                _G_exactly_1465, lastError = self.exactly('a')
                self.considerError(lastError, None)
                return (_G_exactly_1465, self.currentError)
            _G_or_1466, lastError = self._or([_G_or_1462, _G_or_1464])
            self.considerError(lastError, 'A')
            return (_G_or_1466, self.currentError)


        def rule_B(self):
            _locals = {'self': self}
            self.locals['B'] = _locals
            def _G_or_1467():
                self._trace('it\n\n', (11941, 11945), self.input.position)
                _G_exactly_1468, lastError = self.exactly('B')
                self.considerError(lastError, None)
                return (_G_exactly_1468, self.currentError)
            def _G_or_1469():
                self._trace('  Oc', (11947, 11951), self.input.position)
                _G_exactly_1470, lastError = self.exactly('b')
                self.considerError(lastError, None)
                return (_G_exactly_1470, self.currentError)
            _G_or_1471, lastError = self._or([_G_or_1467, _G_or_1469])
            self.considerError(lastError, 'B')
            return (_G_or_1471, self.currentError)


        def rule_C(self):
            _locals = {'self': self}
            self.locals['C'] = _locals
            def _G_or_1472():
                self._trace('tege', (11956, 11960), self.input.position)
                _G_exactly_1473, lastError = self.exactly('C')
                self.considerError(lastError, None)
                return (_G_exactly_1473, self.currentError)
            def _G_or_1474():
                self._trace("= '0", (11962, 11966), self.input.position)
                _G_exactly_1475, lastError = self.exactly('c')
                self.considerError(lastError, None)
                return (_G_exactly_1475, self.currentError)
            _G_or_1476, lastError = self._or([_G_or_1472, _G_or_1474])
            self.considerError(lastError, 'C')
            return (_G_or_1476, self.currentError)


        def rule_D(self):
            _locals = {'self': self}
            self.locals['D'] = _locals
            def _G_or_1477():
                self._trace('talD', (11971, 11975), self.input.position)
                _G_exactly_1478, lastError = self.exactly('D')
                self.considerError(lastError, None)
                return (_G_exactly_1478, self.currentError)
            def _G_or_1479():
                self._trace('it+>', (11977, 11981), self.input.position)
                _G_exactly_1480, lastError = self.exactly('d')
                self.considerError(lastError, None)
                return (_G_exactly_1480, self.currentError)
            _G_or_1481, lastError = self._or([_G_or_1477, _G_or_1479])
            self.considerError(lastError, 'D')
            return (_G_or_1481, self.currentError)


        def rule_E(self):
            _locals = {'self': self}
            self.locals['E'] = _locals
            def _G_or_1482():
                self._trace('> in', (11986, 11990), self.input.position)
                _G_exactly_1483, lastError = self.exactly('E')
                self.considerError(lastError, None)
                return (_G_exactly_1483, self.currentError)
            def _G_or_1484():
                self._trace('ds, ', (11992, 11996), self.input.position)
                _G_exactly_1485, lastError = self.exactly('e')
                self.considerError(lastError, None)
                return (_G_exactly_1485, self.currentError)
            _G_or_1486, lastError = self._or([_G_or_1482, _G_or_1484])
            self.considerError(lastError, 'E')
            return (_G_or_1486, self.currentError)


        def rule_F(self):
            _locals = {'self': self}
            self.locals['F'] = _locals
            def _G_or_1487():
                self._trace('   H', (12001, 12005), self.input.position)
                _G_exactly_1488, lastError = self.exactly('F')
                self.considerError(lastError, None)
                return (_G_exactly_1488, self.currentError)
            def _G_or_1489():
                self._trace('Digi', (12007, 12011), self.input.position)
                _G_exactly_1490, lastError = self.exactly('f')
                self.considerError(lastError, None)
                return (_G_exactly_1490, self.currentError)
            _G_or_1491, lastError = self._or([_G_or_1487, _G_or_1489])
            self.considerError(lastError, 'F')
            return (_G_or_1491, self.currentError)


        def rule_G(self):
            _locals = {'self': self}
            self.locals['G'] = _locals
            def _G_or_1492():
                self._trace('igit', (12016, 12020), self.input.position)
                _G_exactly_1493, lastError = self.exactly('G')
                self.considerError(lastError, None)
                return (_G_exactly_1493, self.currentError)
            def _G_or_1494():
                self._trace(' A |', (12022, 12026), self.input.position)
                _G_exactly_1495, lastError = self.exactly('g')
                self.considerError(lastError, None)
                return (_G_exactly_1495, self.currentError)
            _G_or_1496, lastError = self._or([_G_or_1492, _G_or_1494])
            self.considerError(lastError, 'G')
            return (_G_or_1496, self.currentError)


        def rule_H(self):
            _locals = {'self': self}
            self.locals['H'] = _locals
            def _G_or_1497():
                self._trace('C | ', (12031, 12035), self.input.position)
                _G_exactly_1498, lastError = self.exactly('H')
                self.considerError(lastError, None)
                return (_G_exactly_1498, self.currentError)
            def _G_or_1499():
                self._trace('| E ', (12037, 12041), self.input.position)
                _G_exactly_1500, lastError = self.exactly('h')
                self.considerError(lastError, None)
                return (_G_exactly_1500, self.currentError)
            _G_or_1501, lastError = self._or([_G_or_1497, _G_or_1499])
            self.considerError(lastError, 'H')
            return (_G_or_1501, self.currentError)


        def rule_I(self):
            _locals = {'self': self}
            self.locals['I'] = _locals
            def _G_or_1502():
                self._trace('    ', (12046, 12050), self.input.position)
                _G_exactly_1503, lastError = self.exactly('I')
                self.considerError(lastError, None)
                return (_G_exactly_1503, self.currentError)
            def _G_or_1504():
                self._trace('xInt', (12052, 12056), self.input.position)
                _G_exactly_1505, lastError = self.exactly('i')
                self.considerError(lastError, None)
                return (_G_exactly_1505, self.currentError)
            _G_or_1506, lastError = self._or([_G_or_1502, _G_or_1504])
            self.considerError(lastError, 'I')
            return (_G_or_1506, self.currentError)


        def rule_K(self):
            _locals = {'self': self}
            self.locals['K'] = _locals
            def _G_or_1507():
                self._trace("= '0", (12061, 12065), self.input.position)
                _G_exactly_1508, lastError = self.exactly('K')
                self.considerError(lastError, None)
                return (_G_exactly_1508, self.currentError)
            def _G_or_1509():
                self._trace('X <H', (12067, 12071), self.input.position)
                _G_exactly_1510, lastError = self.exactly('k')
                self.considerError(lastError, None)
                return (_G_exactly_1510, self.currentError)
            _G_or_1511, lastError = self._or([_G_or_1507, _G_or_1509])
            self.considerError(lastError, 'K')
            return (_G_or_1511, self.currentError)


        def rule_L(self):
            _locals = {'self': self}
            self.locals['L'] = _locals
            def _G_or_1512():
                self._trace('it+>', (12076, 12080), self.input.position)
                _G_exactly_1513, lastError = self.exactly('L')
                self.considerError(lastError, None)
                return (_G_exactly_1513, self.currentError)
            def _G_or_1514():
                self._trace('s ->', (12082, 12086), self.input.position)
                _G_exactly_1515, lastError = self.exactly('l')
                self.considerError(lastError, None)
                return (_G_exactly_1515, self.currentError)
            _G_or_1516, lastError = self._or([_G_or_1512, _G_or_1514])
            self.considerError(lastError, 'L')
            return (_G_or_1516, self.currentError)


        def rule_M(self):
            _locals = {'self': self}
            self.locals['M'] = _locals
            def _G_or_1517():
                self._trace('ds, ', (12091, 12095), self.input.position)
                _G_exactly_1518, lastError = self.exactly('M')
                self.considerError(lastError, None)
                return (_G_exactly_1518, self.currentError)
            def _G_or_1519():
                self._trace(')\n\n ', (12097, 12101), self.input.position)
                _G_exactly_1520, lastError = self.exactly('m')
                self.considerError(lastError, None)
                return (_G_exactly_1520, self.currentError)
            _G_or_1521, lastError = self._or([_G_or_1517, _G_or_1519])
            self.considerError(lastError, 'M')
            return (_G_or_1521, self.currentError)


        def rule_N(self):
            _locals = {'self': self}
            self.locals['N'] = _locals
            def _G_or_1522():
                self._trace('cima', (12106, 12110), self.input.position)
                _G_exactly_1523, lastError = self.exactly('N')
                self.considerError(lastError, None)
                return (_G_exactly_1523, self.currentError)
            def _G_or_1524():
                self._trace('nteg', (12112, 12116), self.input.position)
                _G_exactly_1525, lastError = self.exactly('n')
                self.considerError(lastError, None)
                return (_G_exactly_1525, self.currentError)
            _G_or_1526, lastError = self._or([_G_or_1522, _G_or_1524])
            self.considerError(lastError, 'N')
            return (_G_or_1526, self.currentError)


        def rule_O(self):
            _locals = {'self': self}
            self.locals['O'] = _locals
            def _G_or_1527():
                self._trace('<dig', (12121, 12125), self.input.position)
                _G_exactly_1528, lastError = self.exactly('O')
                self.considerError(lastError, None)
                return (_G_exactly_1528, self.currentError)
            def _G_or_1529():
                self._trace('+>:d', (12127, 12131), self.input.position)
                _G_exactly_1530, lastError = self.exactly('o')
                self.considerError(lastError, None)
                return (_G_exactly_1530, self.currentError)
            _G_or_1531, lastError = self._or([_G_or_1527, _G_or_1529])
            self.considerError(lastError, 'O')
            return (_G_or_1531, self.currentError)


        def rule_P(self):
            _locals = {'self': self}
            self.locals['P'] = _locals
            def _G_or_1532():
                self._trace('int(', (12136, 12140), self.input.position)
                _G_exactly_1533, lastError = self.exactly('P')
                self.considerError(lastError, None)
                return (_G_exactly_1533, self.currentError)
            def _G_or_1534():
                self._trace(')\n\n ', (12142, 12146), self.input.position)
                _G_exactly_1535, lastError = self.exactly('p')
                self.considerError(lastError, None)
                return (_G_exactly_1535, self.currentError)
            _G_or_1536, lastError = self._or([_G_or_1532, _G_or_1534])
            self.considerError(lastError, 'P')
            return (_G_or_1536, self.currentError)


        def rule_R(self):
            _locals = {'self': self}
            self.locals['R'] = _locals
            def _G_or_1537():
                self._trace('uble', (12151, 12155), self.input.position)
                _G_exactly_1538, lastError = self.exactly('R')
                self.considerError(lastError, None)
                return (_G_exactly_1538, self.currentError)
            def _G_or_1539():
                self._trace('tera', (12157, 12161), self.input.position)
                _G_exactly_1540, lastError = self.exactly('r')
                self.considerError(lastError, None)
                return (_G_exactly_1540, self.currentError)
            _G_or_1541, lastError = self._or([_G_or_1537, _G_or_1539])
            self.considerError(lastError, 'R')
            return (_G_or_1541, self.currentError)


        def rule_S(self):
            _locals = {'self': self}
            self.locals['S'] = _locals
            def _G_or_1542():
                self._trace('xpon', (12166, 12170), self.input.position)
                _G_exactly_1543, lastError = self.exactly('S')
                self.considerError(lastError, None)
                return (_G_exactly_1543, self.currentError)
            def _G_or_1544():
                self._trace('tDec', (12172, 12176), self.input.position)
                _G_exactly_1545, lastError = self.exactly('s')
                self.considerError(lastError, None)
                return (_G_exactly_1545, self.currentError)
            _G_or_1546, lastError = self._or([_G_or_1542, _G_or_1544])
            self.considerError(lastError, 'S')
            return (_G_or_1546, self.currentError)


        def rule_T(self):
            _locals = {'self': self}
            self.locals['T'] = _locals
            def _G_or_1547():
                self._trace('eal\n', (12181, 12185), self.input.position)
                _G_exactly_1548, lastError = self.exactly('T')
                self.considerError(lastError, None)
                return (_G_exactly_1548, self.currentError)
            def _G_or_1549():
                self._trace('    ', (12187, 12191), self.input.position)
                _G_exactly_1550, lastError = self.exactly('t')
                self.considerError(lastError, None)
                return (_G_exactly_1550, self.currentError)
            _G_or_1551, lastError = self._or([_G_or_1547, _G_or_1549])
            self.considerError(lastError, 'T')
            return (_G_or_1551, self.currentError)


        def rule_U(self):
            _locals = {'self': self}
            self.locals['U'] = _locals
            def _G_or_1552():
                self._trace('    ', (12196, 12200), self.input.position)
                _G_exactly_1553, lastError = self.exactly('U')
                self.considerError(lastError, None)
                return (_G_exactly_1553, self.currentError)
            def _G_or_1554():
                self._trace(' | R', (12202, 12206), self.input.position)
                _G_exactly_1555, lastError = self.exactly('u')
                self.considerError(lastError, None)
                return (_G_exactly_1555, self.currentError)
            _G_or_1556, lastError = self._or([_G_or_1552, _G_or_1554])
            self.considerError(lastError, 'U')
            return (_G_or_1556, self.currentError)


        def rule_V(self):
            _locals = {'self': self}
            self.locals['V'] = _locals
            def _G_or_1557():
                self._trace('rDec', (12211, 12215), self.input.position)
                _G_exactly_1558, lastError = self.exactly('V')
                self.considerError(lastError, None)
                return (_G_exactly_1558, self.currentError)
            def _G_or_1559():
                self._trace('alRe', (12217, 12221), self.input.position)
                _G_exactly_1560, lastError = self.exactly('v')
                self.considerError(lastError, None)
                return (_G_exactly_1560, self.currentError)
            _G_or_1561, lastError = self._or([_G_or_1557, _G_or_1559])
            self.considerError(lastError, 'V')
            return (_G_or_1561, self.currentError)


        def rule_W(self):
            _locals = {'self': self}
            self.locals['W'] = _locals
            def _G_or_1562():
                self._trace('   E', (12226, 12230), self.input.position)
                _G_exactly_1563, lastError = self.exactly('W')
                self.considerError(lastError, None)
                return (_G_exactly_1563, self.currentError)
            def _G_or_1564():
                self._trace('onen', (12232, 12236), self.input.position)
                _G_exactly_1565, lastError = self.exactly('w')
                self.considerError(lastError, None)
                return (_G_exactly_1565, self.currentError)
            _G_or_1566, lastError = self._or([_G_or_1562, _G_or_1564])
            self.considerError(lastError, 'W')
            return (_G_or_1566, self.currentError)


        def rule_X(self):
            _locals = {'self': self}
            self.locals['X'] = _locals
            def _G_or_1567():
                self._trace('malR', (12241, 12245), self.input.position)
                _G_exactly_1568, lastError = self.exactly('X')
                self.considerError(lastError, None)
                return (_G_exactly_1568, self.currentError)
            def _G_or_1569():
                self._trace('l = ', (12247, 12251), self.input.position)
                _G_exactly_1570, lastError = self.exactly('x')
                self.considerError(lastError, None)
                return (_G_exactly_1570, self.currentError)
            _G_or_1571, lastError = self._or([_G_or_1567, _G_or_1569])
            self.considerError(lastError, 'X')
            return (_G_or_1571, self.currentError)


        def rule_Y(self):
            _locals = {'self': self}
            self.locals['Y'] = _locals
            def _G_or_1572():
                self._trace('imal', (12256, 12260), self.input.position)
                _G_exactly_1573, lastError = self.exactly('Y')
                self.considerError(lastError, None)
                return (_G_exactly_1573, self.currentError)
            def _G_or_1574():
                self._trace('tege', (12262, 12266), self.input.position)
                _G_exactly_1575, lastError = self.exactly('y')
                self.considerError(lastError, None)
                return (_G_exactly_1575, self.currentError)
            _G_or_1576, lastError = self._or([_G_or_1572, _G_or_1574])
            self.considerError(lastError, 'Y')
            return (_G_or_1576, self.currentError)


        def rule_Z(self):
            _locals = {'self': self}
            self.locals['Z'] = _locals
            def _G_or_1577():
                self._trace('egul', (12271, 12275), self.input.position)
                _G_exactly_1578, lastError = self.exactly('Z')
                self.considerError(lastError, None)
                return (_G_exactly_1578, self.currentError)
            def _G_or_1579():
                self._trace('Deci', (12277, 12281), self.input.position)
                _G_exactly_1580, lastError = self.exactly('z')
                self.considerError(lastError, None)
                return (_G_exactly_1580, self.currentError)
            _G_or_1581, lastError = self._or([_G_or_1577, _G_or_1579])
            self.considerError(lastError, 'Z')
            return (_G_or_1581, self.currentError)


        _G_expr_9 = compile('s', '<string>', 'eval')
        _G_expr_27 = compile('["UnionAll", sq, rq]', '<string>', 'eval')
        _G_expr_39 = compile('["Union", sq, rq]', '<string>', 'eval')
        _G_expr_55 = compile('["SingleQuery", m, w, r]', '<string>', 'eval')
        _G_expr_81 = compile('["Match", p, w]', '<string>', 'eval')
        _G_expr_96 = compile('["Unwind", ex, v]', '<string>', 'eval')
        _G_expr_109 = compile('["Merge", [head] + tail]', '<string>', 'eval')
        _G_expr_122 = compile('["MergeActionMatch", s]', '<string>', 'eval')
        _G_expr_136 = compile('["MergeActionCreate", s]', '<string>', 'eval')
        _G_expr_147 = compile('["Create", p]', '<string>', 'eval')
        _G_expr_160 = compile('["Set", [head] + tail]', '<string>', 'eval')
        _G_expr_166 = compile('["SetItemPropertyExpression", pex, ex]', '<string>', 'eval')
        _G_expr_172 = compile('["SetItem", v, ex]', '<string>', 'eval')
        _G_expr_207 = compile('["Delete", [head] + tail]', '<string>', 'eval')
        _G_expr_223 = compile('["Remove", [head] + tail]', '<string>', 'eval')
        _G_expr_228 = compile('["RemoveItemVar", v, nl]', '<string>', 'eval')
        _G_expr_232 = compile('["RemoveItemPe", p]', '<string>', 'eval')
        _G_expr_257 = compile('["With", d, rb, w]', '<string>', 'eval')
        _G_expr_279 = compile('["Return", d, rb]', '<string>', 'eval')
        _G_expr_297 = compile('["ReturnBody", ri, o, s, l]', '<string>', 'eval')
        _G_expr_310 = compile('["ReturnItems", [head] + tail]', '<string>', 'eval')
        _G_expr_319 = compile('["ReturnItem", ex, s]', '<string>', 'eval')
        _G_expr_323 = compile('["ReturnItem", ex, None]', '<string>', 'eval')
        _G_expr_341 = compile('["Order", [head] + tail]', '<string>', 'eval')
        _G_expr_349 = compile('["Skip", ex]', '<string>', 'eval')
        _G_expr_358 = compile('["Limit", ex]', '<string>', 'eval')
        _G_expr_381 = compile('["sort", ex, "desc"]', '<string>', 'eval')
        _G_expr_405 = compile('["sort", ex, "asc"]', '<string>', 'eval')
        _G_expr_415 = compile('["Where", ex]', '<string>', 'eval')
        _G_expr_423 = compile('[head] + tail', '<string>', 'eval')
        _G_expr_431 = compile('["PatternPart", v, ap]', '<string>', 'eval')
        _G_expr_438 = compile('["GraphPatternPart", v, ap]', '<string>', 'eval')
        _G_expr_442 = compile('["PatternPart", None, ap]', '<string>', 'eval')
        _G_expr_452 = compile('["PatternElement", np, pec]', '<string>', 'eval')
        _G_expr_458 = compile('pe', '<string>', 'eval')
        _G_expr_472 = compile('nl', '<string>', 'eval')
        _G_expr_479 = compile('p', '<string>', 'eval')
        _G_expr_484 = compile('["NodePattern", s, nl, p]', '<string>', 'eval')
        _G_expr_489 = compile('["PatternElementChain", rp, np]', '<string>', 'eval')
        _G_expr_509 = compile('["RelationshipsPattern", la, rd, ra]', '<string>', 'eval')
        _G_expr_535 = compile('["RelationshipDetail", v, q, rt, rl, p]', '<string>', 'eval')
        _G_expr_554 = compile('["RelationshipTypes", head] + tail', '<string>', 'eval')
        _G_expr_564 = compile('["NodeLabel", n]', '<string>', 'eval')
        _G_expr_579 = compile('slice(start, stop)', '<string>', 'eval')
        _G_expr_591 = compile('["or", ex1, ex2]', '<string>', 'eval')
        _G_expr_604 = compile('["xor", ex1, ex2]', '<string>', 'eval')
        _G_expr_617 = compile('["and", ex1, ex2]', '<string>', 'eval')
        _G_expr_628 = compile('["not", ex]', '<string>', 'eval')
        _G_expr_639 = compile('["eq",  ex1, ex2]', '<string>', 'eval')
        _G_expr_647 = compile('["neq", ex1, ex2]', '<string>', 'eval')
        _G_expr_662 = compile('["lt",  ex1, ex2]', '<string>', 'eval')
        _G_expr_670 = compile('["gt",  ex1, ex2]', '<string>', 'eval')
        _G_expr_678 = compile('["lte", ex1, ex2]', '<string>', 'eval')
        _G_expr_686 = compile('["gte", ex1, ex2]', '<string>', 'eval')
        _G_expr_697 = compile('["add", ex1, ex2]', '<string>', 'eval')
        _G_expr_705 = compile('["sub", ex1, ex2]', '<string>', 'eval')
        _G_expr_716 = compile('["multi", ex1, ex2]', '<string>', 'eval')
        _G_expr_724 = compile('["div",   ex1, ex2]', '<string>', 'eval')
        _G_expr_732 = compile('["mod",   ex1, ex2]', '<string>', 'eval')
        _G_expr_743 = compile('["hat", ex1, ex2]', '<string>', 'eval')
        _G_expr_756 = compile('["minus", ex]', '<string>', 'eval')
        _G_expr_769 = compile('["PropertyLookup", prop_name]', '<string>', 'eval')
        _G_expr_784 = compile('["slice", start, end]', '<string>', 'eval')
        _G_expr_836 = compile('[operator, ex2]', '<string>', 'eval')
        _G_expr_864 = compile('["Expression3", ex1, c]', '<string>', 'eval')
        _G_expr_878 = compile('["Expression2", a, c]', '<string>', 'eval')
        _G_expr_935 = compile('item', '<string>', 'eval')
        _G_expr_943 = compile('["List", ex]', '<string>', 'eval')
        _G_expr_958 = compile('["Filter", fex]', '<string>', 'eval')
        _G_expr_980 = compile('["Extract", fex, ex]', '<string>', 'eval')
        _G_expr_992 = compile('["All", fex]', '<string>', 'eval')
        _G_expr_1004 = compile('["Any", fex]', '<string>', 'eval')
        _G_expr_1017 = compile('["None", fex]', '<string>', 'eval')
        _G_expr_1032 = compile('["Single", fex]', '<string>', 'eval')
        _G_expr_1050 = compile('ex', '<string>', 'eval')
        _G_expr_1058 = compile('["RelationshipsPattern", np, pec]', '<string>', 'eval')
        _G_expr_1069 = compile('["GraphRelationshipsPattern", v, np, pec]', '<string>', 'eval')
        _G_expr_1077 = compile('["FilterExpression", i, w]', '<string>', 'eval')
        _G_expr_1085 = compile('["IdInColl", v, ex]', '<string>', 'eval')
        _G_expr_1117 = compile('["call", func, distinct, args]', '<string>', 'eval')
        _G_expr_1129 = compile('["ListComprehension", fex, ex]', '<string>', 'eval')
        _G_expr_1135 = compile('["PropertyLookup", n]', '<string>', 'eval')
        _G_expr_1164 = compile('["Case", ex, cas, el]', '<string>', 'eval')
        _G_expr_1179 = compile('[ex1, ex2]', '<string>', 'eval')
        _G_expr_1182 = compile('["Variable", s]', '<string>', 'eval')
        _G_expr_1201 = compile('"".join(cs)', '<string>', 'eval')
        _G_expr_1222 = compile('["Literal", l]', '<string>', 'eval')
        _G_expr_1264 = compile('(k, v)', '<string>', 'eval')
        _G_expr_1283 = compile('["Literal", dict(pairs)]', '<string>', 'eval')
        _G_expr_1294 = compile('["Parameter", p]', '<string>', 'eval')
        _G_expr_1301 = compile('["Expression", a, opts]', '<string>', 'eval')
        _G_expr_1325 = compile('int(ds, 8)', '<string>', 'eval')
        _G_expr_1349 = compile('int(ds, 16)', '<string>', 'eval')
        _G_expr_1356 = compile('int(ds)', '<string>', 'eval')
        _G_expr_1372 = compile('float(ds)', '<string>', 'eval')
    if Grammar.globals is not None:
        Grammar.globals = Grammar.globals.copy()
        Grammar.globals.update(ruleGlobals)
    else:
        Grammar.globals = ruleGlobals
    return Grammar