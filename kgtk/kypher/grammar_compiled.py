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
                self._trace('on', (2364, 2366), self.input.position)
                _G_apply_337, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace(':ex ', (2366, 2370), self.input.position)
                _G_exactly_338, lastError = self.exactly(',')
                self.considerError(lastError, None)
                self._trace('SP ', (2370, 2373), self.input.position)
                _G_apply_339, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('A S SP Sy', (2373, 2382), self.input.position)
                _G_apply_340, lastError = self._apply(self.rule_SortItem, "SortItem", [])
                self.considerError(lastError, None)
                return (_G_apply_340, self.currentError)
            _G_many_341, lastError = self.many(_G_many_336)
            self.considerError(lastError, 'Order')
            _locals['tail'] = _G_many_341
            _G_python_343, lastError = eval(self._G_expr_342, self.globals, _locals), None
            self.considerError(lastError, 'Order')
            return (_G_python_343, self.currentError)


        def rule_Skip(self):
            _locals = {'self': self}
            self.locals['Skip'] = _locals
            self._trace('   ', (2425, 2428), self.input.position)
            _G_apply_344, lastError = self._apply(self.rule_S, "S", [])
            self.considerError(lastError, 'Skip')
            self._trace('  ', (2428, 2430), self.input.position)
            _G_apply_345, lastError = self._apply(self.rule_K, "K", [])
            self.considerError(lastError, 'Skip')
            self._trace('  ', (2430, 2432), self.input.position)
            _G_apply_346, lastError = self._apply(self.rule_I, "I", [])
            self.considerError(lastError, 'Skip')
            self._trace('  ', (2432, 2434), self.input.position)
            _G_apply_347, lastError = self._apply(self.rule_P, "P", [])
            self.considerError(lastError, 'Skip')
            self._trace(' | ', (2434, 2437), self.input.position)
            _G_apply_348, lastError = self._apply(self.rule_SP, "SP", [])
            self.considerError(lastError, 'Skip')
            self._trace('Expression:', (2437, 2448), self.input.position)
            _G_apply_349, lastError = self._apply(self.rule_Expression, "Expression", [])
            self.considerError(lastError, 'Skip')
            _locals['ex'] = _G_apply_349
            _G_python_351, lastError = eval(self._G_expr_350, self.globals, _locals), None
            self.considerError(lastError, 'Skip')
            return (_G_python_351, self.currentError)


        def rule_Limit(self):
            _locals = {'self': self}
            self.locals['Limit'] = _locals
            self._trace('e]\n', (2476, 2479), self.input.position)
            _G_apply_352, lastError = self._apply(self.rule_L, "L", [])
            self.considerError(lastError, 'Limit')
            self._trace('\n ', (2479, 2481), self.input.position)
            _G_apply_353, lastError = self._apply(self.rule_I, "I", [])
            self.considerError(lastError, 'Limit')
            self._trace('  ', (2481, 2483), self.input.position)
            _G_apply_354, lastError = self._apply(self.rule_M, "M", [])
            self.considerError(lastError, 'Limit')
            self._trace(' O', (2483, 2485), self.input.position)
            _G_apply_355, lastError = self._apply(self.rule_I, "I", [])
            self.considerError(lastError, 'Limit')
            self._trace('rd', (2485, 2487), self.input.position)
            _G_apply_356, lastError = self._apply(self.rule_T, "T", [])
            self.considerError(lastError, 'Limit')
            self._trace('er ', (2487, 2490), self.input.position)
            _G_apply_357, lastError = self._apply(self.rule_SP, "SP", [])
            self.considerError(lastError, 'Limit')
            self._trace('=  O R D E ', (2490, 2501), self.input.position)
            _G_apply_358, lastError = self._apply(self.rule_Expression, "Expression", [])
            self.considerError(lastError, 'Limit')
            _locals['ex'] = _G_apply_358
            _G_python_360, lastError = eval(self._G_expr_359, self.globals, _locals), None
            self.considerError(lastError, 'Limit')
            return (_G_python_360, self.currentError)


        def rule_SortItem(self):
            _locals = {'self': self}
            self.locals['SortItem'] = _locals
            def _G_or_361():
                self._trace("' WS SortIt", (2533, 2544), self.input.position)
                _G_apply_362, lastError = self._apply(self.rule_Expression, "Expression", [])
                self.considerError(lastError, None)
                _locals['ex'] = _G_apply_362
                def _G_or_363():
                    self._trace('ta', (2549, 2551), self.input.position)
                    _G_apply_364, lastError = self._apply(self.rule_SP, "SP", [])
                    self.considerError(lastError, None)
                    self._trace('il', (2551, 2553), self.input.position)
                    _G_apply_365, lastError = self._apply(self.rule_D, "D", [])
                    self.considerError(lastError, None)
                    self._trace(' -', (2553, 2555), self.input.position)
                    _G_apply_366, lastError = self._apply(self.rule_E, "E", [])
                    self.considerError(lastError, None)
                    self._trace('> ', (2555, 2557), self.input.position)
                    _G_apply_367, lastError = self._apply(self.rule_S, "S", [])
                    self.considerError(lastError, None)
                    self._trace('["', (2557, 2559), self.input.position)
                    _G_apply_368, lastError = self._apply(self.rule_C, "C", [])
                    self.considerError(lastError, None)
                    self._trace('Or', (2559, 2561), self.input.position)
                    _G_apply_369, lastError = self._apply(self.rule_E, "E", [])
                    self.considerError(lastError, None)
                    self._trace('de', (2561, 2563), self.input.position)
                    _G_apply_370, lastError = self._apply(self.rule_N, "N", [])
                    self.considerError(lastError, None)
                    self._trace('r"', (2563, 2565), self.input.position)
                    _G_apply_371, lastError = self._apply(self.rule_D, "D", [])
                    self.considerError(lastError, None)
                    self._trace(', ', (2565, 2567), self.input.position)
                    _G_apply_372, lastError = self._apply(self.rule_I, "I", [])
                    self.considerError(lastError, None)
                    self._trace('[h', (2567, 2569), self.input.position)
                    _G_apply_373, lastError = self._apply(self.rule_N, "N", [])
                    self.considerError(lastError, None)
                    self._trace('ea', (2569, 2571), self.input.position)
                    _G_apply_374, lastError = self._apply(self.rule_G, "G", [])
                    self.considerError(lastError, None)
                    return (_G_apply_374, self.currentError)
                def _G_or_375():
                    self._trace(' + ', (2573, 2576), self.input.position)
                    _G_apply_376, lastError = self._apply(self.rule_SP, "SP", [])
                    self.considerError(lastError, None)
                    self._trace('ta', (2576, 2578), self.input.position)
                    _G_apply_377, lastError = self._apply(self.rule_D, "D", [])
                    self.considerError(lastError, None)
                    self._trace('il', (2578, 2580), self.input.position)
                    _G_apply_378, lastError = self._apply(self.rule_E, "E", [])
                    self.considerError(lastError, None)
                    self._trace(']\n', (2580, 2582), self.input.position)
                    _G_apply_379, lastError = self._apply(self.rule_S, "S", [])
                    self.considerError(lastError, None)
                    self._trace('\n ', (2582, 2584), self.input.position)
                    _G_apply_380, lastError = self._apply(self.rule_C, "C", [])
                    self.considerError(lastError, None)
                    return (_G_apply_380, self.currentError)
                _G_or_381, lastError = self._or([_G_or_363, _G_or_375])
                self.considerError(lastError, None)
                _G_python_383, lastError = eval(self._G_expr_382, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_383, self.currentError)
            def _G_or_384():
                self._trace('-> ["Skip",', (2620, 2631), self.input.position)
                _G_apply_385, lastError = self._apply(self.rule_Expression, "Expression", [])
                self.considerError(lastError, None)
                _locals['ex'] = _G_apply_385
                def _G_optional_386():
                    def _G_or_387():
                        self._trace('\n ', (2636, 2638), self.input.position)
                        _G_apply_388, lastError = self._apply(self.rule_SP, "SP", [])
                        self.considerError(lastError, None)
                        self._trace('  ', (2638, 2640), self.input.position)
                        _G_apply_389, lastError = self._apply(self.rule_A, "A", [])
                        self.considerError(lastError, None)
                        self._trace(' L', (2640, 2642), self.input.position)
                        _G_apply_390, lastError = self._apply(self.rule_S, "S", [])
                        self.considerError(lastError, None)
                        self._trace('im', (2642, 2644), self.input.position)
                        _G_apply_391, lastError = self._apply(self.rule_C, "C", [])
                        self.considerError(lastError, None)
                        self._trace('it', (2644, 2646), self.input.position)
                        _G_apply_392, lastError = self._apply(self.rule_E, "E", [])
                        self.considerError(lastError, None)
                        self._trace(' =', (2646, 2648), self.input.position)
                        _G_apply_393, lastError = self._apply(self.rule_N, "N", [])
                        self.considerError(lastError, None)
                        self._trace('  ', (2648, 2650), self.input.position)
                        _G_apply_394, lastError = self._apply(self.rule_D, "D", [])
                        self.considerError(lastError, None)
                        self._trace('L ', (2650, 2652), self.input.position)
                        _G_apply_395, lastError = self._apply(self.rule_I, "I", [])
                        self.considerError(lastError, None)
                        self._trace('I ', (2652, 2654), self.input.position)
                        _G_apply_396, lastError = self._apply(self.rule_N, "N", [])
                        self.considerError(lastError, None)
                        self._trace('M ', (2654, 2656), self.input.position)
                        _G_apply_397, lastError = self._apply(self.rule_G, "G", [])
                        self.considerError(lastError, None)
                        return (_G_apply_397, self.currentError)
                    def _G_or_398():
                        self._trace('T S', (2658, 2661), self.input.position)
                        _G_apply_399, lastError = self._apply(self.rule_SP, "SP", [])
                        self.considerError(lastError, None)
                        self._trace('P ', (2661, 2663), self.input.position)
                        _G_apply_400, lastError = self._apply(self.rule_A, "A", [])
                        self.considerError(lastError, None)
                        self._trace('Ex', (2663, 2665), self.input.position)
                        _G_apply_401, lastError = self._apply(self.rule_S, "S", [])
                        self.considerError(lastError, None)
                        self._trace('pr', (2665, 2667), self.input.position)
                        _G_apply_402, lastError = self._apply(self.rule_C, "C", [])
                        self.considerError(lastError, None)
                        return (_G_apply_402, self.currentError)
                    _G_or_403, lastError = self._or([_G_or_387, _G_or_398])
                    self.considerError(lastError, None)
                    return (_G_or_403, self.currentError)
                def _G_optional_404():
                    return (None, self.input.nullError())
                _G_or_405, lastError = self._or([_G_optional_386, _G_optional_404])
                self.considerError(lastError, None)
                _G_python_407, lastError = eval(self._G_expr_406, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_407, self.currentError)
            _G_or_408, lastError = self._or([_G_or_361, _G_or_384])
            self.considerError(lastError, 'SortItem')
            return (_G_or_408, self.currentError)


        def rule_Where(self):
            _locals = {'self': self}
            self.locals['Where'] = _locals
            self._trace('rt', (2701, 2703), self.input.position)
            _G_apply_409, lastError = self._apply(self.rule_W, "W", [])
            self.considerError(lastError, 'Where')
            self._trace('It', (2703, 2705), self.input.position)
            _G_apply_410, lastError = self._apply(self.rule_H, "H", [])
            self.considerError(lastError, 'Where')
            self._trace('em', (2705, 2707), self.input.position)
            _G_apply_411, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'Where')
            self._trace(' =', (2707, 2709), self.input.position)
            _G_apply_412, lastError = self._apply(self.rule_R, "R", [])
            self.considerError(lastError, 'Where')
            self._trace(' E', (2709, 2711), self.input.position)
            _G_apply_413, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'Where')
            self._trace('xpr', (2711, 2714), self.input.position)
            _G_apply_414, lastError = self._apply(self.rule_SP, "SP", [])
            self.considerError(lastError, 'Where')
            self._trace('ession:ex (', (2714, 2725), self.input.position)
            _G_apply_415, lastError = self._apply(self.rule_Expression, "Expression", [])
            self.considerError(lastError, 'Where')
            _locals['ex'] = _G_apply_415
            _G_python_417, lastError = eval(self._G_expr_416, self.globals, _locals), None
            self.considerError(lastError, 'Where')
            return (_G_python_417, self.currentError)


        def rule_Pattern(self):
            _locals = {'self': self}
            self.locals['Pattern'] = _locals
            self._trace(' S C) -> ["s', (2756, 2768), self.input.position)
            _G_apply_418, lastError = self._apply(self.rule_PatternPart, "PatternPart", [])
            self.considerError(lastError, 'Pattern')
            _locals['head'] = _G_apply_418
            def _G_many_419():
                self._trace('x, ', (2775, 2778), self.input.position)
                _G_exactly_420, lastError = self.exactly(',')
                self.considerError(lastError, None)
                self._trace('"de', (2778, 2781), self.input.position)
                _G_apply_421, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('sc"]\n       ', (2781, 2793), self.input.position)
                _G_apply_422, lastError = self._apply(self.rule_PatternPart, "PatternPart", [])
                self.considerError(lastError, None)
                return (_G_apply_422, self.currentError)
            _G_many_423, lastError = self.many(_G_many_419)
            self.considerError(lastError, 'Pattern')
            _locals['tail'] = _G_many_423
            _G_python_425, lastError = eval(self._G_expr_424, self.globals, _locals), None
            self.considerError(lastError, 'Pattern')
            return (_G_python_425, self.currentError)


        def rule_PatternPart(self):
            _locals = {'self': self}
            self.locals['PatternPart'] = _locals
            def _G_or_426():
                self._trace(' G | SP ', (2834, 2842), self.input.position)
                _G_apply_427, lastError = self._apply(self.rule_Variable, "Variable", [])
                self.considerError(lastError, None)
                _locals['v'] = _G_apply_427
                self._trace('S C', (2844, 2847), self.input.position)
                _G_apply_428, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace(')? -', (2847, 2851), self.input.position)
                _G_exactly_429, lastError = self.exactly('=')
                self.considerError(lastError, None)
                self._trace('> [', (2851, 2854), self.input.position)
                _G_apply_430, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('"sort", ex, "asc"]\n\n ', (2854, 2875), self.input.position)
                _G_apply_431, lastError = self._apply(self.rule_AnonymousPatternPart, "AnonymousPatternPart", [])
                self.considerError(lastError, None)
                _locals['ap'] = _G_apply_431
                _G_python_433, lastError = eval(self._G_expr_432, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_433, self.currentError)
            def _G_or_434():
                self._trace('re", ex]', (2921, 2929), self.input.position)
                _G_apply_435, lastError = self._apply(self.rule_Variable, "Variable", [])
                self.considerError(lastError, None)
                _locals['v'] = _G_apply_435
                self._trace('    ', (2931, 2935), self.input.position)
                _G_exactly_436, lastError = self.exactly(':')
                self.considerError(lastError, None)
                self._trace('Pat', (2935, 2938), self.input.position)
                _G_apply_437, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('tern = PatternPart:he', (2938, 2959), self.input.position)
                _G_apply_438, lastError = self._apply(self.rule_AnonymousPatternPart, "AnonymousPatternPart", [])
                self.considerError(lastError, None)
                _locals['ap'] = _G_apply_438
                _G_python_440, lastError = eval(self._G_expr_439, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_440, self.currentError)
            def _G_or_441():
                self._trace('   PatternPart = (Var', (3008, 3029), self.input.position)
                _G_apply_442, lastError = self._apply(self.rule_AnonymousPatternPart, "AnonymousPatternPart", [])
                self.considerError(lastError, None)
                _locals['ap'] = _G_apply_442
                _G_python_444, lastError = eval(self._G_expr_443, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_444, self.currentError)
            _G_or_445, lastError = self._or([_G_or_426, _G_or_434, _G_or_441])
            self.considerError(lastError, 'PatternPart')
            return (_G_or_445, self.currentError)


        def rule_AnonymousPatternPart(self):
            _locals = {'self': self}
            self.locals['AnonymousPatternPart'] = _locals
            self._trace('art", v, ap]\n  ', (3085, 3100), self.input.position)
            _G_apply_446, lastError = self._apply(self.rule_PatternElement, "PatternElement", [])
            self.considerError(lastError, 'AnonymousPatternPart')
            return (_G_apply_446, self.currentError)


        def rule_PatternElement(self):
            _locals = {'self': self}
            self.locals['PatternElement'] = _locals
            def _G_or_447():
                self._trace("iable:v ':' WS AnonymousPatternP", (3120, 3152), self.input.position)
                _G_apply_448, lastError = self._apply(self.rule_NodePattern, "NodePattern", [])
                self.considerError(lastError, None)
                _locals['np'] = _G_apply_448
                def _G_many_449():
                    self._trace('Pa', (3177, 3179), self.input.position)
                    _G_apply_450, lastError = self._apply(self.rule_WS, "WS", [])
                    self.considerError(lastError, None)
                    self._trace('rt", v, ap]\n        ', (3179, 3199), self.input.position)
                    _G_apply_451, lastError = self._apply(self.rule_PatternElementChain, "PatternElementChain", [])
                    self.considerError(lastError, None)
                    return (_G_apply_451, self.currentError)
                _G_many_452, lastError = self.many(_G_many_449)
                self.considerError(lastError, None)
                _locals['pec'] = _G_many_452
                _G_python_454, lastError = eval(self._G_expr_453, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_454, self.currentError)
            def _G_or_455():
                self._trace('mous', (3272, 3276), self.input.position)
                _G_exactly_456, lastError = self.exactly('(')
                self.considerError(lastError, None)
                self._trace('PatternPart = P', (3276, 3291), self.input.position)
                _G_apply_457, lastError = self._apply(self.rule_PatternElement, "PatternElement", [])
                self.considerError(lastError, None)
                _locals['pe'] = _G_apply_457
                self._trace('ernE', (3294, 3298), self.input.position)
                _G_exactly_458, lastError = self.exactly(')')
                self.considerError(lastError, None)
                _G_python_460, lastError = eval(self._G_expr_459, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_460, self.currentError)
            _G_or_461, lastError = self._or([_G_or_447, _G_or_455])
            self.considerError(lastError, 'PatternElement')
            return (_G_or_461, self.currentError)


        def rule_NodePattern(self):
            _locals = {'self': self}
            self.locals['NodePattern'] = _locals
            self._trace('emen', (3319, 3323), self.input.position)
            _G_exactly_462, lastError = self.exactly('(')
            self.considerError(lastError, 'NodePattern')
            self._trace('t =', (3323, 3326), self.input.position)
            _G_apply_463, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'NodePattern')
            def _G_optional_464():
                self._trace('            NodePattern:np\n  ', (3341, 3370), self.input.position)
                _G_apply_465, lastError = self._apply(self.rule_SymbolicName, "SymbolicName", [])
                self.considerError(lastError, None)
                _locals['s'] = _G_apply_465
                self._trace('   ', (3372, 3375), self.input.position)
                _G_apply_466, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                _G_python_467, lastError = eval(self._G_expr_9, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_467, self.currentError)
            def _G_optional_468():
                return (None, self.input.nullError())
            _G_or_469, lastError = self._or([_G_optional_464, _G_optional_468])
            self.considerError(lastError, 'NodePattern')
            _locals['s'] = _G_or_469
            def _G_optional_470():
                self._trace('in)*:pec\n                   ', (3413, 3441), self.input.position)
                _G_apply_471, lastError = self._apply(self.rule_NodeLabels, "NodeLabels", [])
                self.considerError(lastError, None)
                _locals['nl'] = _G_apply_471
                self._trace('-> ', (3444, 3447), self.input.position)
                _G_apply_472, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                _G_python_474, lastError = eval(self._G_expr_473, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_474, self.currentError)
            def _G_optional_475():
                return (None, self.input.nullError())
            _G_or_476, lastError = self._or([_G_optional_470, _G_optional_475])
            self.considerError(lastError, 'NodePattern')
            _locals['nl'] = _G_or_476
            def _G_optional_477():
                self._trace("        | '(' PatternElement", (3487, 3515), self.input.position)
                _G_apply_478, lastError = self._apply(self.rule_Properties, "Properties", [])
                self.considerError(lastError, None)
                _locals['p'] = _G_apply_478
                self._trace("e '", (3517, 3520), self.input.position)
                _G_apply_479, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                _G_python_481, lastError = eval(self._G_expr_480, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_481, self.currentError)
            def _G_optional_482():
                return (None, self.input.nullError())
            _G_or_483, lastError = self._or([_G_optional_477, _G_optional_482])
            self.considerError(lastError, 'NodePattern')
            _locals['p'] = _G_or_483
            self._trace("rn = '(' WS\n    ", (3543, 3559), self.input.position)
            _G_exactly_484, lastError = self.exactly(')')
            self.considerError(lastError, 'NodePattern')
            _G_python_486, lastError = eval(self._G_expr_485, self.globals, _locals), None
            self.considerError(lastError, 'NodePattern')
            return (_G_python_486, self.currentError)


        def rule_PatternElementChain(self):
            _locals = {'self': self}
            self.locals['PatternElementChain'] = _locals
            self._trace(' -> s\n              ', (3611, 3631), self.input.position)
            _G_apply_487, lastError = self._apply(self.rule_RelationshipPattern, "RelationshipPattern", [])
            self.considerError(lastError, 'PatternElementChain')
            _locals['rp'] = _G_apply_487
            self._trace(')?:', (3634, 3637), self.input.position)
            _G_apply_488, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'PatternElementChain')
            self._trace('s\n          ', (3637, 3649), self.input.position)
            _G_apply_489, lastError = self._apply(self.rule_NodePattern, "NodePattern", [])
            self.considerError(lastError, 'PatternElementChain')
            _locals['np'] = _G_apply_489
            _G_python_491, lastError = eval(self._G_expr_490, self.globals, _locals), None
            self.considerError(lastError, 'PatternElementChain')
            return (_G_python_491, self.currentError)


        def rule_RelationshipPattern(self):
            _locals = {'self': self}
            self.locals['RelationshipPattern'] = _locals
            def _G_optional_492():
                self._trace('         )?:nl', (3710, 3724), self.input.position)
                _G_apply_493, lastError = self._apply(self.rule_LeftArrowHead, "LeftArrowHead", [])
                self.considerError(lastError, None)
                return (_G_apply_493, self.currentError)
            def _G_optional_494():
                return (None, self.input.nullError())
            _G_or_495, lastError = self._or([_G_optional_492, _G_optional_494])
            self.considerError(lastError, 'RelationshipPattern')
            _locals['la'] = _G_or_495
            self._trace('   ', (3728, 3731), self.input.position)
            _G_apply_496, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'RelationshipPattern')
            self._trace('     ', (3731, 3736), self.input.position)
            _G_apply_497, lastError = self._apply(self.rule_Dash, "Dash", [])
            self.considerError(lastError, 'RelationshipPattern')
            self._trace('   ', (3736, 3739), self.input.position)
            _G_apply_498, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'RelationshipPattern')
            def _G_optional_499():
                self._trace('   (\n              ', (3739, 3758), self.input.position)
                _G_apply_500, lastError = self._apply(self.rule_RelationshipDetail, "RelationshipDetail", [])
                self.considerError(lastError, None)
                return (_G_apply_500, self.currentError)
            def _G_optional_501():
                return (None, self.input.nullError())
            _G_or_502, lastError = self._or([_G_optional_499, _G_optional_501])
            self.considerError(lastError, 'RelationshipPattern')
            _locals['rd'] = _G_or_502
            self._trace('   ', (3762, 3765), self.input.position)
            _G_apply_503, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'RelationshipPattern')
            self._trace('Prope', (3765, 3770), self.input.position)
            _G_apply_504, lastError = self._apply(self.rule_Dash, "Dash", [])
            self.considerError(lastError, 'RelationshipPattern')
            self._trace('rti', (3770, 3773), self.input.position)
            _G_apply_505, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'RelationshipPattern')
            def _G_optional_506():
                self._trace('es:p WS -> p\n  ', (3773, 3788), self.input.position)
                _G_apply_507, lastError = self._apply(self.rule_RightArrowHead, "RightArrowHead", [])
                self.considerError(lastError, None)
                return (_G_apply_507, self.currentError)
            def _G_optional_508():
                return (None, self.input.nullError())
            _G_or_509, lastError = self._or([_G_optional_506, _G_optional_508])
            self.considerError(lastError, 'RelationshipPattern')
            _locals['ra'] = _G_or_509
            _G_python_511, lastError = eval(self._G_expr_510, self.globals, _locals), None
            self.considerError(lastError, 'RelationshipPattern')
            return (_G_python_511, self.currentError)


        def rule_RelationshipDetail(self):
            _locals = {'self': self}
            self.locals['RelationshipDetail'] = _locals
            self._trace('entC', (3941, 3945), self.input.position)
            _G_exactly_512, lastError = self.exactly('[')
            self.considerError(lastError, 'RelationshipDetail')
            def _G_optional_513():
                self._trace('hain", rp, np]\n\n    Relatio', (3945, 3972), self.input.position)
                _G_apply_514, lastError = self._apply(self.rule_Variable, "Variable", [])
                self.considerError(lastError, None)
                return (_G_apply_514, self.currentError)
            def _G_optional_515():
                return (None, self.input.nullError())
            _G_or_516, lastError = self._or([_G_optional_513, _G_optional_515])
            self.considerError(lastError, 'RelationshipDetail')
            _locals['v'] = _G_or_516
            def _G_optional_517():
                self._trace('ipPattern = LeftArrowH', (3975, 3997), self.input.position)
                _G_exactly_518, lastError = self.exactly('?')
                self.considerError(lastError, None)
                return (_G_exactly_518, self.currentError)
            def _G_optional_519():
                return (None, self.input.nullError())
            _G_or_520, lastError = self._or([_G_optional_517, _G_optional_519])
            self.considerError(lastError, 'RelationshipDetail')
            _locals['q'] = _G_or_520
            def _G_optional_521():
                self._trace('?:la WS Dash WS RelationshipDetail?:', (4000, 4036), self.input.position)
                _G_apply_522, lastError = self._apply(self.rule_RelationshipTypes, "RelationshipTypes", [])
                self.considerError(lastError, None)
                return (_G_apply_522, self.currentError)
            def _G_optional_523():
                return (None, self.input.nullError())
            _G_or_524, lastError = self._or([_G_optional_521, _G_optional_523])
            self.considerError(lastError, 'RelationshipDetail')
            _locals['rt'] = _G_or_524
            def _G_optional_525():
                self._trace('Hea', (4060, 4063), self.input.position)
                _G_exactly_526, lastError = self.exactly('*')
                self.considerError(lastError, None)
                self._trace('d?:ra -> ["Re', (4063, 4076), self.input.position)
                _G_apply_527, lastError = self._apply(self.rule_RangeLiteral, "RangeLiteral", [])
                self.considerError(lastError, None)
                return (_G_apply_527, self.currentError)
            def _G_optional_528():
                return (None, self.input.nullError())
            _G_or_529, lastError = self._or([_G_optional_525, _G_optional_528])
            self.considerError(lastError, 'RelationshipDetail')
            _locals['rl'] = _G_or_529
            self._trace('nsh', (4081, 4084), self.input.position)
            _G_apply_530, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'RelationshipDetail')
            def _G_optional_531():
                self._trace('ipsPattern", la, rd, ra]\n\n   ', (4084, 4113), self.input.position)
                _G_apply_532, lastError = self._apply(self.rule_Properties, "Properties", [])
                self.considerError(lastError, None)
                return (_G_apply_532, self.currentError)
            def _G_optional_533():
                return (None, self.input.nullError())
            _G_or_534, lastError = self._or([_G_optional_531, _G_optional_533])
            self.considerError(lastError, 'RelationshipDetail')
            _locals['p'] = _G_or_534
            self._trace('TO DO: fix WS handling', (4116, 4138), self.input.position)
            _G_exactly_535, lastError = self.exactly(']')
            self.considerError(lastError, 'RelationshipDetail')
            _G_python_537, lastError = eval(self._G_expr_536, self.globals, _locals), None
            self.considerError(lastError, 'RelationshipDetail')
            return (_G_python_537, self.currentError)


        def rule_Properties(self):
            _locals = {'self': self}
            self.locals['Properties'] = _locals
            def _G_or_538():
                self._trace('tern:\n    R', (4195, 4206), self.input.position)
                _G_apply_539, lastError = self._apply(self.rule_MapLiteral, "MapLiteral", [])
                self.considerError(lastError, None)
                return (_G_apply_539, self.currentError)
            def _G_or_540():
                self._trace("tail = '['", (4219, 4229), self.input.position)
                _G_apply_541, lastError = self._apply(self.rule_Parameter, "Parameter", [])
                self.considerError(lastError, None)
                return (_G_apply_541, self.currentError)
            _G_or_542, lastError = self._or([_G_or_538, _G_or_540])
            self.considerError(lastError, 'Properties')
            return (_G_or_542, self.currentError)


        def rule_RelationshipTypes(self):
            _locals = {'self': self}
            self.locals['RelationshipTypes'] = _locals
            self._trace('  Va', (4250, 4254), self.input.position)
            _G_exactly_543, lastError = self.exactly(':')
            self.considerError(lastError, 'RelationshipTypes')
            self._trace('riable?:v\n  ', (4254, 4266), self.input.position)
            _G_apply_544, lastError = self._apply(self.rule_RelTypeName, "RelTypeName", [])
            self.considerError(lastError, 'RelationshipTypes')
            _locals['head'] = _G_apply_544
            def _G_many_545():
                self._trace('  ', (4273, 4275), self.input.position)
                _G_apply_546, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('    ', (4275, 4279), self.input.position)
                _G_exactly_547, lastError = self.exactly('|')
                self.considerError(lastError, None)
                def _G_optional_548():
                    self._trace('    ', (4279, 4283), self.input.position)
                    _G_exactly_549, lastError = self.exactly(':')
                    self.considerError(lastError, None)
                    return (_G_exactly_549, self.currentError)
                def _G_optional_550():
                    return (None, self.input.nullError())
                _G_or_551, lastError = self._or([_G_optional_548, _G_optional_550])
                self.considerError(lastError, None)
                self._trace("  '", (4284, 4287), self.input.position)
                _G_apply_552, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace("?'?:q\n      ", (4287, 4299), self.input.position)
                _G_apply_553, lastError = self._apply(self.rule_RelTypeName, "RelTypeName", [])
                self.considerError(lastError, None)
                return (_G_apply_553, self.currentError)
            _G_many_554, lastError = self.many(_G_many_545)
            self.considerError(lastError, 'RelationshipTypes')
            _locals['tail'] = _G_many_554
            _G_python_556, lastError = eval(self._G_expr_555, self.globals, _locals), None
            self.considerError(lastError, 'RelationshipTypes')
            return (_G_python_556, self.currentError)


        def rule_NodeLabels(self):
            _locals = {'self': self}
            self.locals['NodeLabels'] = _locals
            self._trace(" ('*' Rang", (4358, 4368), self.input.position)
            _G_apply_557, lastError = self._apply(self.rule_NodeLabel, "NodeLabel", [])
            self.considerError(lastError, 'NodeLabels')
            _locals['head'] = _G_apply_557
            def _G_many_558():
                self._trace('l)', (4375, 4377), self.input.position)
                _G_apply_559, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('?:rl WS\n  ', (4377, 4387), self.input.position)
                _G_apply_560, lastError = self._apply(self.rule_NodeLabel, "NodeLabel", [])
                self.considerError(lastError, None)
                return (_G_apply_560, self.currentError)
            _G_many_561, lastError = self.many(_G_many_558)
            self.considerError(lastError, 'NodeLabels')
            _locals['tail'] = _G_many_561
            _G_python_562, lastError = eval(self._G_expr_424, self.globals, _locals), None
            self.considerError(lastError, 'NodeLabels')
            return (_G_python_562, self.currentError)


        def rule_NodeLabel(self):
            _locals = {'self': self}
            self.locals['NodeLabel'] = _locals
            self._trace('    ', (4424, 4428), self.input.position)
            _G_exactly_563, lastError = self.exactly(':')
            self.considerError(lastError, 'NodeLabel')
            self._trace('          ', (4428, 4438), self.input.position)
            _G_apply_564, lastError = self._apply(self.rule_LabelName, "LabelName", [])
            self.considerError(lastError, 'NodeLabel')
            _locals['n'] = _G_apply_564
            _G_python_566, lastError = eval(self._G_expr_565, self.globals, _locals), None
            self.considerError(lastError, 'NodeLabel')
            return (_G_python_566, self.currentError)


        def rule_RangeLiteral(self):
            _locals = {'self': self}
            self.locals['RangeLiteral'] = _locals
            def _G_optional_567():
                self._trace(' r', (4478, 4480), self.input.position)
                _G_apply_568, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('t, rl, p]\n\n    ', (4480, 4495), self.input.position)
                _G_apply_569, lastError = self._apply(self.rule_IntegerLiteral, "IntegerLiteral", [])
                self.considerError(lastError, None)
                return (_G_apply_569, self.currentError)
            def _G_optional_570():
                return (None, self.input.nullError())
            _G_or_571, lastError = self._or([_G_optional_567, _G_optional_570])
            self.considerError(lastError, 'RangeLiteral')
            _locals['start'] = _G_or_571
            self._trace('es ', (4503, 4506), self.input.position)
            _G_apply_572, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'RangeLiteral')
            def _G_optional_573():
                self._trace('MapL', (4508, 4512), self.input.position)
                _G_exactly_574, lastError = self.exactly('..')
                self.considerError(lastError, None)
                self._trace('ite', (4512, 4515), self.input.position)
                _G_apply_575, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('ral\n           ', (4515, 4530), self.input.position)
                _G_apply_576, lastError = self._apply(self.rule_IntegerLiteral, "IntegerLiteral", [])
                self.considerError(lastError, None)
                return (_G_apply_576, self.currentError)
            def _G_optional_577():
                return (None, self.input.nullError())
            _G_or_578, lastError = self._or([_G_optional_573, _G_optional_577])
            self.considerError(lastError, 'RangeLiteral')
            _locals['stop'] = _G_or_578
            self._trace('ara', (4537, 4540), self.input.position)
            _G_apply_579, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'RangeLiteral')
            _G_python_581, lastError = eval(self._G_expr_580, self.globals, _locals), None
            self.considerError(lastError, 'RangeLiteral')
            return (_G_python_581, self.currentError)


        def rule_LabelName(self):
            _locals = {'self': self}
            self.locals['LabelName'] = _locals
            self._trace('RelTypeName:h', (4575, 4588), self.input.position)
            _G_apply_582, lastError = self._apply(self.rule_SymbolicName, "SymbolicName", [])
            self.considerError(lastError, 'LabelName')
            return (_G_apply_582, self.currentError)


        def rule_RelTypeName(self):
            _locals = {'self': self}
            self.locals['RelTypeName'] = _locals
            self._trace('? WS RelTypeN', (4603, 4616), self.input.position)
            _G_apply_583, lastError = self._apply(self.rule_SymbolicName, "SymbolicName", [])
            self.considerError(lastError, 'RelTypeName')
            return (_G_apply_583, self.currentError)


        def rule_Expression(self):
            _locals = {'self': self}
            self.locals['Expression'] = _locals
            self._trace('["Relationshi', (4630, 4643), self.input.position)
            _G_apply_584, lastError = self._apply(self.rule_Expression12, "Expression12", [])
            self.considerError(lastError, 'Expression')
            return (_G_apply_584, self.currentError)


        def rule_Expression12(self):
            _locals = {'self': self}
            self.locals['Expression12'] = _locals
            def _G_or_585():
                self._trace(' tail\n\n    No', (4659, 4672), self.input.position)
                _G_apply_586, lastError = self._apply(self.rule_Expression11, "Expression11", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_586
                self._trace('bel', (4676, 4679), self.input.position)
                _G_apply_587, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('s ', (4679, 4681), self.input.position)
                _G_apply_588, lastError = self._apply(self.rule_O, "O", [])
                self.considerError(lastError, None)
                self._trace('= ', (4681, 4683), self.input.position)
                _G_apply_589, lastError = self._apply(self.rule_R, "R", [])
                self.considerError(lastError, None)
                self._trace('Nod', (4683, 4686), self.input.position)
                _G_apply_590, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('eLabel:head (', (4686, 4699), self.input.position)
                _G_apply_591, lastError = self._apply(self.rule_Expression12, "Expression12", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_591
                _G_python_593, lastError = eval(self._G_expr_592, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_593, self.currentError)
            def _G_or_594():
                self._trace('   NodeLabel ', (4738, 4751), self.input.position)
                _G_apply_595, lastError = self._apply(self.rule_Expression11, "Expression11", [])
                self.considerError(lastError, None)
                return (_G_apply_595, self.currentError)
            _G_or_596, lastError = self._or([_G_or_585, _G_or_594])
            self.considerError(lastError, 'Expression12')
            return (_G_or_596, self.currentError)


        def rule_Expression11(self):
            _locals = {'self': self}
            self.locals['Expression11'] = _locals
            def _G_or_597():
                self._trace('n -> ["NodeLa', (4767, 4780), self.input.position)
                _G_apply_598, lastError = self._apply(self.rule_Expression10, "Expression10", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_598
                self._trace(', n', (4784, 4787), self.input.position)
                _G_apply_599, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace(']\n', (4787, 4789), self.input.position)
                _G_apply_600, lastError = self._apply(self.rule_X, "X", [])
                self.considerError(lastError, None)
                self._trace('\n ', (4789, 4791), self.input.position)
                _G_apply_601, lastError = self._apply(self.rule_O, "O", [])
                self.considerError(lastError, None)
                self._trace('  ', (4791, 4793), self.input.position)
                _G_apply_602, lastError = self._apply(self.rule_R, "R", [])
                self.considerError(lastError, None)
                self._trace(' Ra', (4793, 4796), self.input.position)
                _G_apply_603, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('ngeLiteral = ', (4796, 4809), self.input.position)
                _G_apply_604, lastError = self._apply(self.rule_Expression11, "Expression11", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_604
                _G_python_606, lastError = eval(self._G_expr_605, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_606, self.currentError)
            def _G_or_607():
                self._trace('ntegerLiteral', (4849, 4862), self.input.position)
                _G_apply_608, lastError = self._apply(self.rule_Expression10, "Expression10", [])
                self.considerError(lastError, None)
                return (_G_apply_608, self.currentError)
            _G_or_609, lastError = self._or([_G_or_597, _G_or_607])
            self.considerError(lastError, 'Expression11')
            return (_G_or_609, self.currentError)


        def rule_Expression10(self):
            _locals = {'self': self}
            self.locals['Expression10'] = _locals
            def _G_or_610():
                self._trace('ice(start, s', (4878, 4890), self.input.position)
                _G_apply_611, lastError = self._apply(self.rule_Expression9, "Expression9", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_611
                self._trace('\n\n ', (4894, 4897), self.input.position)
                _G_apply_612, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('  ', (4897, 4899), self.input.position)
                _G_apply_613, lastError = self._apply(self.rule_A, "A", [])
                self.considerError(lastError, None)
                self._trace(' L', (4899, 4901), self.input.position)
                _G_apply_614, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace('ab', (4901, 4903), self.input.position)
                _G_apply_615, lastError = self._apply(self.rule_D, "D", [])
                self.considerError(lastError, None)
                self._trace('elN', (4903, 4906), self.input.position)
                _G_apply_616, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('ame = Symboli', (4906, 4919), self.input.position)
                _G_apply_617, lastError = self._apply(self.rule_Expression10, "Expression10", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_617
                _G_python_619, lastError = eval(self._G_expr_618, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_619, self.currentError)
            def _G_or_620():
                self._trace('   Expressio', (4959, 4971), self.input.position)
                _G_apply_621, lastError = self._apply(self.rule_Expression9, "Expression9", [])
                self.considerError(lastError, None)
                return (_G_apply_621, self.currentError)
            _G_or_622, lastError = self._or([_G_or_610, _G_or_620])
            self.considerError(lastError, 'Expression10')
            return (_G_or_622, self.currentError)


        def rule_Expression9(self):
            _locals = {'self': self}
            self.locals['Expression9'] = _locals
            def _G_or_623():
                self._trace('2\n', (4986, 4988), self.input.position)
                _G_apply_624, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace('\n ', (4988, 4990), self.input.position)
                _G_apply_625, lastError = self._apply(self.rule_O, "O", [])
                self.considerError(lastError, None)
                self._trace('  ', (4990, 4992), self.input.position)
                _G_apply_626, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                self._trace(' Ex', (4992, 4995), self.input.position)
                _G_apply_627, lastError = self._apply(self.rule_SP, "SP", [])
                self.considerError(lastError, None)
                self._trace('pression12 =', (4995, 5007), self.input.position)
                _G_apply_628, lastError = self._apply(self.rule_Expression9, "Expression9", [])
                self.considerError(lastError, None)
                _locals['ex'] = _G_apply_628
                _G_python_630, lastError = eval(self._G_expr_629, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_630, self.currentError)
            def _G_or_631():
                self._trace('ession12:ex2', (5039, 5051), self.input.position)
                _G_apply_632, lastError = self._apply(self.rule_Expression8, "Expression8", [])
                self.considerError(lastError, None)
                return (_G_apply_632, self.currentError)
            _G_or_633, lastError = self._or([_G_or_623, _G_or_631])
            self.considerError(lastError, 'Expression9')
            return (_G_or_633, self.currentError)


        def rule_Expression8(self):
            _locals = {'self': self}
            self.locals['Expression8'] = _locals
            def _G_or_634():
                self._trace(' ex2]\n      ', (5066, 5078), self.input.position)
                _G_apply_635, lastError = self._apply(self.rule_Expression7, "Expression7", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_635
                self._trace('   ', (5082, 5085), self.input.position)
                _G_apply_636, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('    ', (5085, 5089), self.input.position)
                _G_exactly_637, lastError = self.exactly('=')
                self.considerError(lastError, None)
                self._trace('| Ex', (5089, 5093), self.input.position)
                _G_apply_638, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('pression11\n\n', (5093, 5105), self.input.position)
                _G_apply_639, lastError = self._apply(self.rule_Expression8, "Expression8", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_639
                _G_python_641, lastError = eval(self._G_expr_640, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_641, self.currentError)
            def _G_or_642():
                self._trace('X O R SP Exp', (5144, 5156), self.input.position)
                _G_apply_643, lastError = self._apply(self.rule_Expression7, "Expression7", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_643
                self._trace('ion', (5160, 5163), self.input.position)
                _G_apply_644, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('11:ex', (5163, 5168), self.input.position)
                _G_exactly_645, lastError = self.exactly('<>')
                self.considerError(lastError, None)
                self._trace('2 -', (5168, 5171), self.input.position)
                _G_apply_646, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('> ["xor", ex', (5171, 5183), self.input.position)
                _G_apply_647, lastError = self._apply(self.rule_Expression8, "Expression8", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_647
                _G_python_649, lastError = eval(self._G_expr_648, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_649, self.currentError)
            def _G_or_650():
                self._trace('\n\n    Expres', (5222, 5234), self.input.position)
                _G_apply_651, lastError = self._apply(self.rule_Expression7, "Expression7", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_651
                self._trace('10 ', (5238, 5241), self.input.position)
                _G_apply_652, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('= Exp', (5241, 5246), self.input.position)
                _G_exactly_653, lastError = self.exactly('!=')
                self.considerError(lastError, None)
                self._trace('res', (5246, 5249), self.input.position)
                _G_apply_654, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('sion9:ex1 SP', (5249, 5261), self.input.position)
                _G_apply_655, lastError = self._apply(self.rule_Expression8, "Expression8", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_655
                _G_python_656, lastError = eval(self._G_expr_648, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_656, self.currentError)
            def _G_or_657():
                self._trace('x1, ex2]\n   ', (5300, 5312), self.input.position)
                _G_apply_658, lastError = self._apply(self.rule_Expression7, "Expression7", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_658
                self._trace('   ', (5316, 5319), self.input.position)
                _G_apply_659, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('    ', (5319, 5323), self.input.position)
                _G_exactly_660, lastError = self.exactly('<')
                self.considerError(lastError, None)
                self._trace('   |', (5323, 5327), self.input.position)
                _G_apply_661, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace(' Expression9', (5327, 5339), self.input.position)
                _G_apply_662, lastError = self._apply(self.rule_Expression8, "Expression8", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_662
                _G_python_664, lastError = eval(self._G_expr_663, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_664, self.currentError)
            def _G_or_665():
                self._trace('9:ex -> ["no', (5378, 5390), self.input.position)
                _G_apply_666, lastError = self._apply(self.rule_Expression7, "Expression7", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_666
                self._trace('ex]', (5394, 5397), self.input.position)
                _G_apply_667, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('\n   ', (5397, 5401), self.input.position)
                _G_exactly_668, lastError = self.exactly('>')
                self.considerError(lastError, None)
                self._trace('    ', (5401, 5405), self.input.position)
                _G_apply_669, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('         | E', (5405, 5417), self.input.position)
                _G_apply_670, lastError = self._apply(self.rule_Expression8, "Expression8", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_670
                _G_python_672, lastError = eval(self._G_expr_671, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_672, self.currentError)
            def _G_or_673():
                self._trace("n7:ex1 WS '=", (5456, 5468), self.input.position)
                _G_apply_674, lastError = self._apply(self.rule_Expression7, "Expression7", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_674
                self._trace('S E', (5472, 5475), self.input.position)
                _G_apply_675, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('xpres', (5475, 5480), self.input.position)
                _G_exactly_676, lastError = self.exactly('<=')
                self.considerError(lastError, None)
                self._trace('sio', (5480, 5483), self.input.position)
                _G_apply_677, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('n8:ex2 -> ["', (5483, 5495), self.input.position)
                _G_apply_678, lastError = self._apply(self.rule_Expression8, "Expression8", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_678
                _G_python_680, lastError = eval(self._G_expr_679, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_680, self.currentError)
            def _G_or_681():
                self._trace('ssion7:ex1 W', (5534, 5546), self.input.position)
                _G_apply_682, lastError = self._apply(self.rule_Expression7, "Expression7", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_682
                self._trace(">' ", (5550, 5553), self.input.position)
                _G_apply_683, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('WS Ex', (5553, 5558), self.input.position)
                _G_exactly_684, lastError = self.exactly('>=')
                self.considerError(lastError, None)
                self._trace('pre', (5558, 5561), self.input.position)
                _G_apply_685, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('ssion8:ex2 -', (5561, 5573), self.input.position)
                _G_apply_686, lastError = self._apply(self.rule_Expression8, "Expression8", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_686
                _G_python_688, lastError = eval(self._G_expr_687, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_688, self.currentError)
            def _G_or_689():
                self._trace('xpression7:e', (5612, 5624), self.input.position)
                _G_apply_690, lastError = self._apply(self.rule_Expression7, "Expression7", [])
                self.considerError(lastError, None)
                return (_G_apply_690, self.currentError)
            _G_or_691, lastError = self._or([_G_or_634, _G_or_642, _G_or_650, _G_or_657, _G_or_665, _G_or_673, _G_or_681, _G_or_689])
            self.considerError(lastError, 'Expression8')
            return (_G_or_691, self.currentError)


        def rule_Expression7(self):
            _locals = {'self': self}
            self.locals['Expression7'] = _locals
            def _G_or_692():
                self._trace('xpression8:e', (5639, 5651), self.input.position)
                _G_apply_693, lastError = self._apply(self.rule_Expression6, "Expression6", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_693
                self._trace('> [', (5655, 5658), self.input.position)
                _G_apply_694, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('"neq', (5658, 5662), self.input.position)
                _G_exactly_695, lastError = self.exactly('+')
                self.considerError(lastError, None)
                self._trace('", ', (5662, 5665), self.input.position)
                _G_apply_696, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('ex1, ex2]\n  ', (5665, 5677), self.input.position)
                _G_apply_697, lastError = self._apply(self.rule_Expression7, "Expression7", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_697
                _G_python_699, lastError = eval(self._G_expr_698, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_699, self.currentError)
            def _G_or_700():
                self._trace(' WS Expressi', (5716, 5728), self.input.position)
                _G_apply_701, lastError = self._apply(self.rule_Expression6, "Expression6", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_701
                self._trace('ex2', (5732, 5735), self.input.position)
                _G_apply_702, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace(' -> ', (5735, 5739), self.input.position)
                _G_exactly_703, lastError = self.exactly('-')
                self.considerError(lastError, None)
                self._trace('["l', (5739, 5742), self.input.position)
                _G_apply_704, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('t",  ex1, ex', (5742, 5754), self.input.position)
                _G_apply_705, lastError = self._apply(self.rule_Expression7, "Expression7", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_705
                _G_python_707, lastError = eval(self._G_expr_706, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_707, self.currentError)
            def _G_or_708():
                self._trace(" '>'  WS Exp", (5793, 5805), self.input.position)
                _G_apply_709, lastError = self._apply(self.rule_Expression6, "Expression6", [])
                self.considerError(lastError, None)
                return (_G_apply_709, self.currentError)
            _G_or_710, lastError = self._or([_G_or_692, _G_or_700, _G_or_708])
            self.considerError(lastError, 'Expression7')
            return (_G_or_710, self.currentError)


        def rule_Expression6(self):
            _locals = {'self': self}
            self.locals['Expression6'] = _locals
            def _G_or_711():
                self._trace(' ["gt",  ex1', (5820, 5832), self.input.position)
                _G_apply_712, lastError = self._apply(self.rule_Expression5, "Expression5", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_712
                self._trace('2]\n', (5836, 5839), self.input.position)
                _G_apply_713, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('    ', (5839, 5843), self.input.position)
                _G_exactly_714, lastError = self.exactly('*')
                self.considerError(lastError, None)
                self._trace('   ', (5843, 5846), self.input.position)
                _G_apply_715, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('         | E', (5846, 5858), self.input.position)
                _G_apply_716, lastError = self._apply(self.rule_Expression6, "Expression6", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_716
                _G_python_718, lastError = eval(self._G_expr_717, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_718, self.currentError)
            def _G_or_719():
                self._trace(' -> ["lte", ', (5899, 5911), self.input.position)
                _G_apply_720, lastError = self._apply(self.rule_Expression5, "Expression5", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_720
                self._trace(' ex', (5915, 5918), self.input.position)
                _G_apply_721, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('2]\n ', (5918, 5922), self.input.position)
                _G_exactly_722, lastError = self.exactly('/')
                self.considerError(lastError, None)
                self._trace('   ', (5922, 5925), self.input.position)
                _G_apply_723, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('            ', (5925, 5937), self.input.position)
                _G_apply_724, lastError = self._apply(self.rule_Expression6, "Expression6", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_724
                _G_python_726, lastError = eval(self._G_expr_725, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_726, self.currentError)
            def _G_or_727():
                self._trace('ex2 -> ["gte', (5978, 5990), self.input.position)
                _G_apply_728, lastError = self._apply(self.rule_Expression5, "Expression5", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_728
                self._trace('x1,', (5994, 5997), self.input.position)
                _G_apply_729, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace(' ex2', (5997, 6001), self.input.position)
                _G_exactly_730, lastError = self.exactly('%')
                self.considerError(lastError, None)
                self._trace(']\n ', (6001, 6004), self.input.position)
                _G_apply_731, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('            ', (6004, 6016), self.input.position)
                _G_apply_732, lastError = self._apply(self.rule_Expression6, "Expression6", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_732
                _G_python_734, lastError = eval(self._G_expr_733, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_734, self.currentError)
            def _G_or_735():
                self._trace('ssion6:ex1 W', (6057, 6069), self.input.position)
                _G_apply_736, lastError = self._apply(self.rule_Expression5, "Expression5", [])
                self.considerError(lastError, None)
                return (_G_apply_736, self.currentError)
            _G_or_737, lastError = self._or([_G_or_711, _G_or_719, _G_or_727, _G_or_735])
            self.considerError(lastError, 'Expression6')
            return (_G_or_737, self.currentError)


        def rule_Expression5(self):
            _locals = {'self': self}
            self.locals['Expression5'] = _locals
            def _G_or_738():
                self._trace('sion7:ex2 ->', (6084, 6096), self.input.position)
                _G_apply_739, lastError = self._apply(self.rule_Expression4, "Expression4", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_739
                self._trace('dd"', (6100, 6103), self.input.position)
                _G_apply_740, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace(', ex', (6103, 6107), self.input.position)
                _G_exactly_741, lastError = self.exactly('^')
                self.considerError(lastError, None)
                self._trace('1, ', (6107, 6110), self.input.position)
                _G_apply_742, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('ex2]\n       ', (6110, 6122), self.input.position)
                _G_apply_743, lastError = self._apply(self.rule_Expression5, "Expression5", [])
                self.considerError(lastError, None)
                _locals['ex2'] = _G_apply_743
                _G_python_745, lastError = eval(self._G_expr_744, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_745, self.currentError)
            def _G_or_746():
                self._trace('pression7:ex', (6161, 6173), self.input.position)
                _G_apply_747, lastError = self._apply(self.rule_Expression4, "Expression4", [])
                self.considerError(lastError, None)
                return (_G_apply_747, self.currentError)
            _G_or_748, lastError = self._or([_G_or_738, _G_or_746])
            self.considerError(lastError, 'Expression5')
            return (_G_or_748, self.currentError)


        def rule_Expression4(self):
            _locals = {'self': self}
            self.locals['Expression4'] = _locals
            def _G_or_749():
                self._trace('1, e', (6188, 6192), self.input.position)
                _G_exactly_750, lastError = self.exactly('+')
                self.considerError(lastError, None)
                self._trace('x2]', (6192, 6195), self.input.position)
                _G_apply_751, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('\n           ', (6195, 6207), self.input.position)
                _G_apply_752, lastError = self._apply(self.rule_Expression4, "Expression4", [])
                self.considerError(lastError, None)
                return (_G_apply_752, self.currentError)
            def _G_or_753():
                self._trace('ion6', (6221, 6225), self.input.position)
                _G_exactly_754, lastError = self.exactly('-')
                self.considerError(lastError, None)
                self._trace('\n\n ', (6225, 6228), self.input.position)
                _G_apply_755, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('   Expressio', (6228, 6240), self.input.position)
                _G_apply_756, lastError = self._apply(self.rule_Expression4, "Expression4", [])
                self.considerError(lastError, None)
                _locals['ex'] = _G_apply_756
                _G_python_758, lastError = eval(self._G_expr_757, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_758, self.currentError)
            def _G_or_759():
                self._trace('ression6:ex2', (6274, 6286), self.input.position)
                _G_apply_760, lastError = self._apply(self.rule_Expression3, "Expression3", [])
                self.considerError(lastError, None)
                return (_G_apply_760, self.currentError)
            _G_or_761, lastError = self._or([_G_or_749, _G_or_753, _G_or_759])
            self.considerError(lastError, 'Expression4')
            return (_G_or_761, self.currentError)


        def rule_Expression3(self):
            _locals = {'self': self}
            self.locals['Expression3'] = _locals
            def _G_or_762():
                self._trace('x1, ex2]\n   ', (6301, 6313), self.input.position)
                _G_apply_763, lastError = self._apply(self.rule_Expression2, "Expression2", [])
                self.considerError(lastError, None)
                _locals['ex1'] = _G_apply_763
                def _G_many1_764():
                    def _G_or_765():
                        self._trace("ssion5:ex1 WS '/' W", (6333, 6352), self.input.position)
                        _G_apply_766, lastError = self._apply(self.rule_WS, "WS", [])
                        self.considerError(lastError, None)
                        self._trace('S Ex', (6352, 6356), self.input.position)
                        _G_exactly_767, lastError = self.exactly('[')
                        self.considerError(lastError, None)
                        self._trace('pression6:e', (6356, 6367), self.input.position)
                        _G_apply_768, lastError = self._apply(self.rule_Expression, "Expression", [])
                        self.considerError(lastError, None)
                        _locals['prop_name'] = _G_apply_768
                        self._trace('v", ', (6377, 6381), self.input.position)
                        _G_exactly_769, lastError = self.exactly(']')
                        self.considerError(lastError, None)
                        _G_python_771, lastError = eval(self._G_expr_770, self.globals, _locals), None
                        self.considerError(lastError, None)
                        return (_G_python_771, self.currentError)
                    def _G_or_772():
                        self._trace("' W", (6432, 6435), self.input.position)
                        _G_apply_773, lastError = self._apply(self.rule_WS, "WS", [])
                        self.considerError(lastError, None)
                        self._trace('S Ex', (6435, 6439), self.input.position)
                        _G_exactly_774, lastError = self.exactly('[')
                        self.considerError(lastError, None)
                        def _G_optional_775():
                            self._trace('pression6:e', (6439, 6450), self.input.position)
                            _G_apply_776, lastError = self._apply(self.rule_Expression, "Expression", [])
                            self.considerError(lastError, None)
                            return (_G_apply_776, self.currentError)
                        def _G_optional_777():
                            return (None, self.input.nullError())
                        _G_or_778, lastError = self._or([_G_optional_775, _G_optional_777])
                        self.considerError(lastError, None)
                        _locals['start'] = _G_or_778
                        self._trace('"mod"', (6457, 6462), self.input.position)
                        _G_exactly_779, lastError = self.exactly('..')
                        self.considerError(lastError, None)
                        def _G_optional_780():
                            self._trace(',   ex1, ex', (6462, 6473), self.input.position)
                            _G_apply_781, lastError = self._apply(self.rule_Expression, "Expression", [])
                            self.considerError(lastError, None)
                            return (_G_apply_781, self.currentError)
                        def _G_optional_782():
                            return (None, self.input.nullError())
                        _G_or_783, lastError = self._or([_G_optional_780, _G_optional_782])
                        self.considerError(lastError, None)
                        _locals['end'] = _G_or_783
                        self._trace('    ', (6478, 6482), self.input.position)
                        _G_exactly_784, lastError = self.exactly(']')
                        self.considerError(lastError, None)
                        _G_python_786, lastError = eval(self._G_expr_785, self.globals, _locals), None
                        self.considerError(lastError, None)
                        return (_G_python_786, self.currentError)
                    def _G_or_787():
                        def _G_or_788():
                            self._trace("pression4:ex1 WS '^' WS", (6527, 6550), self.input.position)
                            _G_apply_789, lastError = self._apply(self.rule_WS, "WS", [])
                            self.considerError(lastError, None)
                            self._trace(' Expr', (6550, 6555), self.input.position)
                            _G_exactly_790, lastError = self.exactly('=~')
                            self.considerError(lastError, None)
                            _G_python_791, lastError = ("regex"), None
                            self.considerError(lastError, None)
                            return (_G_python_791, self.currentError)
                        def _G_or_792():
                            self._trace('   ', (6588, 6591), self.input.position)
                            _G_apply_793, lastError = self._apply(self.rule_SP, "SP", [])
                            self.considerError(lastError, None)
                            self._trace('  ', (6591, 6593), self.input.position)
                            _G_apply_794, lastError = self._apply(self.rule_I, "I", [])
                            self.considerError(lastError, None)
                            self._trace('  ', (6593, 6595), self.input.position)
                            _G_apply_795, lastError = self._apply(self.rule_N, "N", [])
                            self.considerError(lastError, None)
                            _G_python_796, lastError = ("in"), None
                            self.considerError(lastError, None)
                            return (_G_python_796, self.currentError)
                        def _G_or_797():
                            self._trace('pre', (6625, 6628), self.input.position)
                            _G_apply_798, lastError = self._apply(self.rule_SP, "SP", [])
                            self.considerError(lastError, None)
                            self._trace('ss', (6628, 6630), self.input.position)
                            _G_apply_799, lastError = self._apply(self.rule_S, "S", [])
                            self.considerError(lastError, None)
                            self._trace('io', (6630, 6632), self.input.position)
                            _G_apply_800, lastError = self._apply(self.rule_T, "T", [])
                            self.considerError(lastError, None)
                            self._trace('n4', (6632, 6634), self.input.position)
                            _G_apply_801, lastError = self._apply(self.rule_A, "A", [])
                            self.considerError(lastError, None)
                            self._trace(' =', (6634, 6636), self.input.position)
                            _G_apply_802, lastError = self._apply(self.rule_R, "R", [])
                            self.considerError(lastError, None)
                            self._trace(" '", (6636, 6638), self.input.position)
                            _G_apply_803, lastError = self._apply(self.rule_T, "T", [])
                            self.considerError(lastError, None)
                            self._trace("+'", (6638, 6640), self.input.position)
                            _G_apply_804, lastError = self._apply(self.rule_S, "S", [])
                            self.considerError(lastError, None)
                            self._trace(' WS', (6640, 6643), self.input.position)
                            _G_apply_805, lastError = self._apply(self.rule_SP, "SP", [])
                            self.considerError(lastError, None)
                            self._trace(' E', (6643, 6645), self.input.position)
                            _G_apply_806, lastError = self._apply(self.rule_W, "W", [])
                            self.considerError(lastError, None)
                            self._trace('xp', (6645, 6647), self.input.position)
                            _G_apply_807, lastError = self._apply(self.rule_I, "I", [])
                            self.considerError(lastError, None)
                            self._trace('re', (6647, 6649), self.input.position)
                            _G_apply_808, lastError = self._apply(self.rule_T, "T", [])
                            self.considerError(lastError, None)
                            self._trace('ss', (6649, 6651), self.input.position)
                            _G_apply_809, lastError = self._apply(self.rule_H, "H", [])
                            self.considerError(lastError, None)
                            _G_python_810, lastError = ("starts_with"), None
                            self.considerError(lastError, None)
                            return (_G_python_810, self.currentError)
                        def _G_or_811():
                            self._trace('n4:', (6690, 6693), self.input.position)
                            _G_apply_812, lastError = self._apply(self.rule_SP, "SP", [])
                            self.considerError(lastError, None)
                            self._trace('ex', (6693, 6695), self.input.position)
                            _G_apply_813, lastError = self._apply(self.rule_E, "E", [])
                            self.considerError(lastError, None)
                            self._trace(' -', (6695, 6697), self.input.position)
                            _G_apply_814, lastError = self._apply(self.rule_N, "N", [])
                            self.considerError(lastError, None)
                            self._trace('> ', (6697, 6699), self.input.position)
                            _G_apply_815, lastError = self._apply(self.rule_D, "D", [])
                            self.considerError(lastError, None)
                            self._trace('["', (6699, 6701), self.input.position)
                            _G_apply_816, lastError = self._apply(self.rule_S, "S", [])
                            self.considerError(lastError, None)
                            self._trace('min', (6701, 6704), self.input.position)
                            _G_apply_817, lastError = self._apply(self.rule_SP, "SP", [])
                            self.considerError(lastError, None)
                            self._trace('us', (6704, 6706), self.input.position)
                            _G_apply_818, lastError = self._apply(self.rule_W, "W", [])
                            self.considerError(lastError, None)
                            self._trace('",', (6706, 6708), self.input.position)
                            _G_apply_819, lastError = self._apply(self.rule_I, "I", [])
                            self.considerError(lastError, None)
                            self._trace(' e', (6708, 6710), self.input.position)
                            _G_apply_820, lastError = self._apply(self.rule_T, "T", [])
                            self.considerError(lastError, None)
                            self._trace('x]', (6710, 6712), self.input.position)
                            _G_apply_821, lastError = self._apply(self.rule_H, "H", [])
                            self.considerError(lastError, None)
                            _G_python_822, lastError = ("ends_with"), None
                            self.considerError(lastError, None)
                            return (_G_python_822, self.currentError)
                        def _G_or_823():
                            self._trace('pre', (6750, 6753), self.input.position)
                            _G_apply_824, lastError = self._apply(self.rule_SP, "SP", [])
                            self.considerError(lastError, None)
                            self._trace('ss', (6753, 6755), self.input.position)
                            _G_apply_825, lastError = self._apply(self.rule_C, "C", [])
                            self.considerError(lastError, None)
                            self._trace('io', (6755, 6757), self.input.position)
                            _G_apply_826, lastError = self._apply(self.rule_O, "O", [])
                            self.considerError(lastError, None)
                            self._trace('n3', (6757, 6759), self.input.position)
                            _G_apply_827, lastError = self._apply(self.rule_N, "N", [])
                            self.considerError(lastError, None)
                            self._trace(' =', (6759, 6761), self.input.position)
                            _G_apply_828, lastError = self._apply(self.rule_T, "T", [])
                            self.considerError(lastError, None)
                            self._trace(' E', (6761, 6763), self.input.position)
                            _G_apply_829, lastError = self._apply(self.rule_A, "A", [])
                            self.considerError(lastError, None)
                            self._trace('xp', (6763, 6765), self.input.position)
                            _G_apply_830, lastError = self._apply(self.rule_I, "I", [])
                            self.considerError(lastError, None)
                            self._trace('re', (6765, 6767), self.input.position)
                            _G_apply_831, lastError = self._apply(self.rule_N, "N", [])
                            self.considerError(lastError, None)
                            self._trace('ss', (6767, 6769), self.input.position)
                            _G_apply_832, lastError = self._apply(self.rule_S, "S", [])
                            self.considerError(lastError, None)
                            _G_python_833, lastError = ("contains"), None
                            self.considerError(lastError, None)
                            return (_G_python_833, self.currentError)
                        _G_or_834, lastError = self._or([_G_or_788, _G_or_792, _G_or_797, _G_or_811, _G_or_823])
                        self.considerError(lastError, None)
                        _locals['operator'] = _G_or_834
                        self._trace('   ', (6811, 6814), self.input.position)
                        _G_apply_835, lastError = self._apply(self.rule_WS, "WS", [])
                        self.considerError(lastError, None)
                        self._trace("    WS '[' E", (6814, 6826), self.input.position)
                        _G_apply_836, lastError = self._apply(self.rule_Expression2, "Expression2", [])
                        self.considerError(lastError, None)
                        _locals['ex2'] = _G_apply_836
                        _G_python_838, lastError = eval(self._G_expr_837, self.globals, _locals), None
                        self.considerError(lastError, None)
                        return (_G_python_838, self.currentError)
                    def _G_or_839():
                        self._trace('up"', (6867, 6870), self.input.position)
                        _G_apply_840, lastError = self._apply(self.rule_SP, "SP", [])
                        self.considerError(lastError, None)
                        self._trace(', ', (6870, 6872), self.input.position)
                        _G_apply_841, lastError = self._apply(self.rule_I, "I", [])
                        self.considerError(lastError, None)
                        self._trace('pr', (6872, 6874), self.input.position)
                        _G_apply_842, lastError = self._apply(self.rule_S, "S", [])
                        self.considerError(lastError, None)
                        self._trace('op_', (6874, 6877), self.input.position)
                        _G_apply_843, lastError = self._apply(self.rule_SP, "SP", [])
                        self.considerError(lastError, None)
                        self._trace('na', (6877, 6879), self.input.position)
                        _G_apply_844, lastError = self._apply(self.rule_N, "N", [])
                        self.considerError(lastError, None)
                        self._trace('me', (6879, 6881), self.input.position)
                        _G_apply_845, lastError = self._apply(self.rule_U, "U", [])
                        self.considerError(lastError, None)
                        self._trace(']\n', (6881, 6883), self.input.position)
                        _G_apply_846, lastError = self._apply(self.rule_L, "L", [])
                        self.considerError(lastError, None)
                        self._trace('  ', (6883, 6885), self.input.position)
                        _G_apply_847, lastError = self._apply(self.rule_L, "L", [])
                        self.considerError(lastError, None)
                        _G_python_848, lastError = (["is_null"]), None
                        self.considerError(lastError, None)
                        return (_G_python_848, self.currentError)
                    def _G_or_849():
                        self._trace('ion', (6919, 6922), self.input.position)
                        _G_apply_850, lastError = self._apply(self.rule_SP, "SP", [])
                        self.considerError(lastError, None)
                        self._trace('?:', (6922, 6924), self.input.position)
                        _G_apply_851, lastError = self._apply(self.rule_I, "I", [])
                        self.considerError(lastError, None)
                        self._trace('st', (6924, 6926), self.input.position)
                        _G_apply_852, lastError = self._apply(self.rule_S, "S", [])
                        self.considerError(lastError, None)
                        self._trace('art', (6926, 6929), self.input.position)
                        _G_apply_853, lastError = self._apply(self.rule_SP, "SP", [])
                        self.considerError(lastError, None)
                        self._trace(" '", (6929, 6931), self.input.position)
                        _G_apply_854, lastError = self._apply(self.rule_N, "N", [])
                        self.considerError(lastError, None)
                        self._trace('..', (6931, 6933), self.input.position)
                        _G_apply_855, lastError = self._apply(self.rule_O, "O", [])
                        self.considerError(lastError, None)
                        self._trace("' ", (6933, 6935), self.input.position)
                        _G_apply_856, lastError = self._apply(self.rule_T, "T", [])
                        self.considerError(lastError, None)
                        self._trace('Exp', (6935, 6938), self.input.position)
                        _G_apply_857, lastError = self._apply(self.rule_SP, "SP", [])
                        self.considerError(lastError, None)
                        self._trace('re', (6938, 6940), self.input.position)
                        _G_apply_858, lastError = self._apply(self.rule_N, "N", [])
                        self.considerError(lastError, None)
                        self._trace('ss', (6940, 6942), self.input.position)
                        _G_apply_859, lastError = self._apply(self.rule_U, "U", [])
                        self.considerError(lastError, None)
                        self._trace('io', (6942, 6944), self.input.position)
                        _G_apply_860, lastError = self._apply(self.rule_L, "L", [])
                        self.considerError(lastError, None)
                        self._trace('n?', (6944, 6946), self.input.position)
                        _G_apply_861, lastError = self._apply(self.rule_L, "L", [])
                        self.considerError(lastError, None)
                        _G_python_862, lastError = (["is_not_null"]), None
                        self.considerError(lastError, None)
                        return (_G_python_862, self.currentError)
                    _G_or_863, lastError = self._or([_G_or_765, _G_or_772, _G_or_787, _G_or_839, _G_or_849])
                    self.considerError(lastError, None)
                    return (_G_or_863, self.currentError)
                _G_many1_864, lastError = self.many(_G_many1_764, _G_many1_764())
                self.considerError(lastError, None)
                _locals['c'] = _G_many1_864
                _G_python_866, lastError = eval(self._G_expr_865, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_866, self.currentError)
            def _G_or_867():
                self._trace(" WS '=~' -> ", (7027, 7039), self.input.position)
                _G_apply_868, lastError = self._apply(self.rule_Expression2, "Expression2", [])
                self.considerError(lastError, None)
                return (_G_apply_868, self.currentError)
            _G_or_869, lastError = self._or([_G_or_762, _G_or_867])
            self.considerError(lastError, 'Expression3')
            return (_G_or_869, self.currentError)


        def rule_Expression2(self):
            _locals = {'self': self}
            self.locals['Expression2'] = _locals
            def _G_or_870():
                self._trace('     ', (7054, 7059), self.input.position)
                _G_apply_871, lastError = self._apply(self.rule_Atom, "Atom", [])
                self.considerError(lastError, None)
                _locals['a'] = _G_apply_871
                def _G_many1_872():
                    def _G_or_873():
                        self._trace('        | SP I', (7063, 7077), self.input.position)
                        _G_apply_874, lastError = self._apply(self.rule_PropertyLookup, "PropertyLookup", [])
                        self.considerError(lastError, None)
                        return (_G_apply_874, self.currentError)
                    def _G_or_875():
                        self._trace(' -> "in"\n  ', (7079, 7090), self.input.position)
                        _G_apply_876, lastError = self._apply(self.rule_NodeLabels, "NodeLabels", [])
                        self.considerError(lastError, None)
                        return (_G_apply_876, self.currentError)
                    _G_or_877, lastError = self._or([_G_or_873, _G_or_875])
                    self.considerError(lastError, None)
                    return (_G_or_877, self.currentError)
                _G_many1_878, lastError = self.many(_G_many1_872, _G_many1_872())
                self.considerError(lastError, None)
                _locals['c'] = _G_many1_878
                _G_python_880, lastError = eval(self._G_expr_879, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_880, self.currentError)
            def _G_or_881():
                self._trace(' T H ', (7135, 7140), self.input.position)
                _G_apply_882, lastError = self._apply(self.rule_Atom, "Atom", [])
                self.considerError(lastError, None)
                return (_G_apply_882, self.currentError)
            _G_or_883, lastError = self._or([_G_or_870, _G_or_881])
            self.considerError(lastError, 'Expression2')
            return (_G_or_883, self.currentError)


        def rule_Atom(self):
            _locals = {'self': self}
            self.locals['Atom'] = _locals
            def _G_or_884():
                self._trace('ts_with"\n     ', (7148, 7162), self.input.position)
                _G_apply_885, lastError = self._apply(self.rule_NumberLiteral, "NumberLiteral", [])
                self.considerError(lastError, None)
                return (_G_apply_885, self.currentError)
            def _G_or_886():
                self._trace('            | ', (7169, 7183), self.input.position)
                _G_apply_887, lastError = self._apply(self.rule_StringLiteral, "StringLiteral", [])
                self.considerError(lastError, None)
                return (_G_apply_887, self.currentError)
            def _G_or_888():
                self._trace('D S SP W I', (7190, 7200), self.input.position)
                _G_apply_889, lastError = self._apply(self.rule_Parameter, "Parameter", [])
                self.considerError(lastError, None)
                return (_G_apply_889, self.currentError)
            def _G_or_890():
                self._trace('> ', (7207, 7209), self.input.position)
                _G_apply_891, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                self._trace('"e', (7209, 7211), self.input.position)
                _G_apply_892, lastError = self._apply(self.rule_R, "R", [])
                self.considerError(lastError, None)
                self._trace('nd', (7211, 7213), self.input.position)
                _G_apply_893, lastError = self._apply(self.rule_U, "U", [])
                self.considerError(lastError, None)
                self._trace('s_', (7213, 7215), self.input.position)
                _G_apply_894, lastError = self._apply(self.rule_E, "E", [])
                self.considerError(lastError, None)
                _G_python_895, lastError = (["Literal", True]), None
                self.considerError(lastError, None)
                return (_G_python_895, self.currentError)
            def _G_or_896():
                self._trace('  ', (7243, 7245), self.input.position)
                _G_apply_897, lastError = self._apply(self.rule_F, "F", [])
                self.considerError(lastError, None)
                self._trace('| ', (7245, 7247), self.input.position)
                _G_apply_898, lastError = self._apply(self.rule_A, "A", [])
                self.considerError(lastError, None)
                self._trace('SP', (7247, 7249), self.input.position)
                _G_apply_899, lastError = self._apply(self.rule_L, "L", [])
                self.considerError(lastError, None)
                self._trace(' C', (7249, 7251), self.input.position)
                _G_apply_900, lastError = self._apply(self.rule_S, "S", [])
                self.considerError(lastError, None)
                self._trace(' O', (7251, 7253), self.input.position)
                _G_apply_901, lastError = self._apply(self.rule_E, "E", [])
                self.considerError(lastError, None)
                _G_python_902, lastError = (["Literal", False]), None
                self.considerError(lastError, None)
                return (_G_python_902, self.currentError)
            def _G_or_903():
                self._trace('  ', (7282, 7284), self.input.position)
                _G_apply_904, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace('  ', (7284, 7286), self.input.position)
                _G_apply_905, lastError = self._apply(self.rule_U, "U", [])
                self.considerError(lastError, None)
                self._trace('  ', (7286, 7288), self.input.position)
                _G_apply_906, lastError = self._apply(self.rule_L, "L", [])
                self.considerError(lastError, None)
                self._trace('  ', (7288, 7290), self.input.position)
                _G_apply_907, lastError = self._apply(self.rule_L, "L", [])
                self.considerError(lastError, None)
                _G_python_908, lastError = (["Literal", None]), None
                self.considerError(lastError, None)
                return (_G_python_908, self.currentError)
            def _G_or_909():
                self._trace('ression2:ex2 ->', (7318, 7333), self.input.position)
                _G_apply_910, lastError = self._apply(self.rule_CaseExpression, "CaseExpression", [])
                self.considerError(lastError, None)
                return (_G_apply_910, self.currentError)
            def _G_or_911():
                self._trace('to', (7340, 7342), self.input.position)
                _G_apply_912, lastError = self._apply(self.rule_C, "C", [])
                self.considerError(lastError, None)
                self._trace('r,', (7342, 7344), self.input.position)
                _G_apply_913, lastError = self._apply(self.rule_O, "O", [])
                self.considerError(lastError, None)
                self._trace(' e', (7344, 7346), self.input.position)
                _G_apply_914, lastError = self._apply(self.rule_U, "U", [])
                self.considerError(lastError, None)
                self._trace('x2', (7346, 7348), self.input.position)
                _G_apply_915, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace(']\n', (7348, 7350), self.input.position)
                _G_apply_916, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                self._trace('    ', (7350, 7354), self.input.position)
                _G_exactly_917, lastError = self.exactly('(')
                self.considerError(lastError, None)
                self._trace('    ', (7354, 7358), self.input.position)
                _G_exactly_918, lastError = self.exactly('*')
                self.considerError(lastError, None)
                self._trace('    ', (7358, 7362), self.input.position)
                _G_exactly_919, lastError = self.exactly(')')
                self.considerError(lastError, None)
                _G_python_920, lastError = (["count *"]), None
                self.considerError(lastError, None)
                return (_G_python_920, self.currentError)
            def _G_or_921():
                self._trace('U L L  -> [', (7384, 7395), self.input.position)
                _G_apply_922, lastError = self._apply(self.rule_MapLiteral, "MapLiteral", [])
                self.considerError(lastError, None)
                return (_G_apply_922, self.currentError)
            def _G_or_923():
                self._trace('l"]\n              ', (7402, 7420), self.input.position)
                _G_apply_924, lastError = self._apply(self.rule_ListComprehension, "ListComprehension", [])
                self.considerError(lastError, None)
                return (_G_apply_924, self.currentError)
            def _G_or_925():
                self._trace(' SP ', (7427, 7431), self.input.position)
                _G_exactly_926, lastError = self.exactly('[')
                self.considerError(lastError, None)
                def _G_or_927():
                    self._trace('P N U L L -> ["is_n', (7445, 7464), self.input.position)
                    _G_apply_928, lastError = self._apply(self.rule_WS, "WS", [])
                    self.considerError(lastError, None)
                    self._trace('ot_null"]\n ', (7464, 7475), self.input.position)
                    _G_apply_929, lastError = self._apply(self.rule_Expression, "Expression", [])
                    self.considerError(lastError, None)
                    _locals['head'] = _G_apply_929
                    self._trace('   ', (7480, 7483), self.input.position)
                    _G_apply_930, lastError = self._apply(self.rule_WS, "WS", [])
                    self.considerError(lastError, None)
                    def _G_many_931():
                        self._trace('"Ex', (7501, 7504), self.input.position)
                        _G_exactly_932, lastError = self.exactly(',')
                        self.considerError(lastError, None)
                        self._trace('pre', (7504, 7507), self.input.position)
                        _G_apply_933, lastError = self._apply(self.rule_WS, "WS", [])
                        self.considerError(lastError, None)
                        self._trace('ssion3", ex', (7507, 7518), self.input.position)
                        _G_apply_934, lastError = self._apply(self.rule_Expression, "Expression", [])
                        self.considerError(lastError, None)
                        _locals['item'] = _G_apply_934
                        self._trace('\n  ', (7523, 7526), self.input.position)
                        _G_apply_935, lastError = self._apply(self.rule_WS, "WS", [])
                        self.considerError(lastError, None)
                        _G_python_937, lastError = eval(self._G_expr_936, self.globals, _locals), None
                        self.considerError(lastError, None)
                        return (_G_python_937, self.currentError)
                    _G_many_938, lastError = self.many(_G_many_931)
                    self.considerError(lastError, None)
                    _locals['tail'] = _G_many_938
                    _G_python_939, lastError = eval(self._G_expr_424, self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_939, self.currentError)
                def _G_or_940():
                    _G_python_941, lastError = ([]), None
                    self.considerError(lastError, None)
                    return (_G_python_941, self.currentError)
                _G_or_942, lastError = self._or([_G_or_927, _G_or_940])
                self.considerError(lastError, None)
                _locals['ex'] = _G_or_942
                self._trace(', a, c]\n    ', (7632, 7644), self.input.position)
                _G_exactly_943, lastError = self.exactly(']')
                self.considerError(lastError, None)
                _G_python_945, lastError = eval(self._G_expr_944, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_945, self.currentError)
            def _G_or_946():
                self._trace('  ', (7667, 7669), self.input.position)
                _G_apply_947, lastError = self._apply(self.rule_F, "F", [])
                self.considerError(lastError, None)
                self._trace(' A', (7669, 7671), self.input.position)
                _G_apply_948, lastError = self._apply(self.rule_I, "I", [])
                self.considerError(lastError, None)
                self._trace('to', (7671, 7673), self.input.position)
                _G_apply_949, lastError = self._apply(self.rule_L, "L", [])
                self.considerError(lastError, None)
                self._trace('m ', (7673, 7675), self.input.position)
                _G_apply_950, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                self._trace('= ', (7675, 7677), self.input.position)
                _G_apply_951, lastError = self._apply(self.rule_E, "E", [])
                self.considerError(lastError, None)
                self._trace('Nu', (7677, 7679), self.input.position)
                _G_apply_952, lastError = self._apply(self.rule_R, "R", [])
                self.considerError(lastError, None)
                self._trace('mbe', (7679, 7682), self.input.position)
                _G_apply_953, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('rLit', (7682, 7686), self.input.position)
                _G_exactly_954, lastError = self.exactly('(')
                self.considerError(lastError, None)
                self._trace('era', (7686, 7689), self.input.position)
                _G_apply_955, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('l\n         | Stri', (7689, 7706), self.input.position)
                _G_apply_956, lastError = self._apply(self.rule_FilterExpression, "FilterExpression", [])
                self.considerError(lastError, None)
                _locals['fex'] = _G_apply_956
                self._trace('ter', (7710, 7713), self.input.position)
                _G_apply_957, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('al\n ', (7713, 7717), self.input.position)
                _G_exactly_958, lastError = self.exactly(')')
                self.considerError(lastError, None)
                _G_python_960, lastError = eval(self._G_expr_959, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_960, self.currentError)
            def _G_or_961():
                self._trace('  ', (7743, 7745), self.input.position)
                _G_apply_962, lastError = self._apply(self.rule_E, "E", [])
                self.considerError(lastError, None)
                self._trace(' |', (7745, 7747), self.input.position)
                _G_apply_963, lastError = self._apply(self.rule_X, "X", [])
                self.considerError(lastError, None)
                self._trace(' T', (7747, 7749), self.input.position)
                _G_apply_964, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                self._trace(' R', (7749, 7751), self.input.position)
                _G_apply_965, lastError = self._apply(self.rule_R, "R", [])
                self.considerError(lastError, None)
                self._trace(' U', (7751, 7753), self.input.position)
                _G_apply_966, lastError = self._apply(self.rule_A, "A", [])
                self.considerError(lastError, None)
                self._trace(' E', (7753, 7755), self.input.position)
                _G_apply_967, lastError = self._apply(self.rule_C, "C", [])
                self.considerError(lastError, None)
                self._trace(' -', (7755, 7757), self.input.position)
                _G_apply_968, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                self._trace('> [', (7757, 7760), self.input.position)
                _G_apply_969, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('"Lit', (7760, 7764), self.input.position)
                _G_exactly_970, lastError = self.exactly('(')
                self.considerError(lastError, None)
                self._trace('era', (7764, 7767), self.input.position)
                _G_apply_971, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('l", True]\n       ', (7767, 7784), self.input.position)
                _G_apply_972, lastError = self._apply(self.rule_FilterExpression, "FilterExpression", [])
                self.considerError(lastError, None)
                _locals['fex'] = _G_apply_972
                self._trace('F A', (7788, 7791), self.input.position)
                _G_apply_973, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                def _G_optional_974():
                    self._trace(' S', (7793, 7795), self.input.position)
                    _G_apply_975, lastError = self._apply(self.rule_WS, "WS", [])
                    self.considerError(lastError, None)
                    self._trace(' E -', (7795, 7799), self.input.position)
                    _G_exactly_976, lastError = self.exactly('|')
                    self.considerError(lastError, None)
                    self._trace('> ["Literal', (7799, 7810), self.input.position)
                    _G_apply_977, lastError = self._apply(self.rule_Expression, "Expression", [])
                    self.considerError(lastError, None)
                    return (_G_apply_977, self.currentError)
                def _G_optional_978():
                    return (None, self.input.nullError())
                _G_or_979, lastError = self._or([_G_optional_974, _G_optional_978])
                self.considerError(lastError, None)
                _locals['ex'] = _G_or_979
                self._trace('lse]', (7815, 7819), self.input.position)
                _G_exactly_980, lastError = self.exactly(')')
                self.considerError(lastError, None)
                _G_python_982, lastError = eval(self._G_expr_981, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_982, self.currentError)
            def _G_or_983():
                self._trace('l"', (7850, 7852), self.input.position)
                _G_apply_984, lastError = self._apply(self.rule_A, "A", [])
                self.considerError(lastError, None)
                self._trace(', ', (7852, 7854), self.input.position)
                _G_apply_985, lastError = self._apply(self.rule_L, "L", [])
                self.considerError(lastError, None)
                self._trace('No', (7854, 7856), self.input.position)
                _G_apply_986, lastError = self._apply(self.rule_L, "L", [])
                self.considerError(lastError, None)
                self._trace('ne]', (7856, 7859), self.input.position)
                _G_apply_987, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('\n   ', (7859, 7863), self.input.position)
                _G_exactly_988, lastError = self.exactly('(')
                self.considerError(lastError, None)
                self._trace('   ', (7863, 7866), self.input.position)
                _G_apply_989, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('   | CaseExpressi', (7866, 7883), self.input.position)
                _G_apply_990, lastError = self._apply(self.rule_FilterExpression, "FilterExpression", [])
                self.considerError(lastError, None)
                _locals['fex'] = _G_apply_990
                self._trace('   ', (7887, 7890), self.input.position)
                _G_apply_991, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('    ', (7890, 7894), self.input.position)
                _G_exactly_992, lastError = self.exactly(')')
                self.considerError(lastError, None)
                _G_python_994, lastError = eval(self._G_expr_993, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_994, self.currentError)
            def _G_or_995():
                self._trace("' ", (7917, 7919), self.input.position)
                _G_apply_996, lastError = self._apply(self.rule_A, "A", [])
                self.considerError(lastError, None)
                self._trace('->', (7919, 7921), self.input.position)
                _G_apply_997, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace(' [', (7921, 7923), self.input.position)
                _G_apply_998, lastError = self._apply(self.rule_Y, "Y", [])
                self.considerError(lastError, None)
                self._trace('"co', (7923, 7926), self.input.position)
                _G_apply_999, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('unt ', (7926, 7930), self.input.position)
                _G_exactly_1000, lastError = self.exactly('(')
                self.considerError(lastError, None)
                self._trace('*"]', (7930, 7933), self.input.position)
                _G_apply_1001, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('\n         | MapLi', (7933, 7950), self.input.position)
                _G_apply_1002, lastError = self._apply(self.rule_FilterExpression, "FilterExpression", [])
                self.considerError(lastError, None)
                _locals['fex'] = _G_apply_1002
                self._trace('l\n ', (7954, 7957), self.input.position)
                _G_apply_1003, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('    ', (7957, 7961), self.input.position)
                _G_exactly_1004, lastError = self.exactly(')')
                self.considerError(lastError, None)
                _G_python_1006, lastError = eval(self._G_expr_1005, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_1006, self.currentError)
            def _G_or_1007():
                self._trace('\n ', (7984, 7986), self.input.position)
                _G_apply_1008, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace('  ', (7986, 7988), self.input.position)
                _G_apply_1009, lastError = self._apply(self.rule_O, "O", [])
                self.considerError(lastError, None)
                self._trace('  ', (7988, 7990), self.input.position)
                _G_apply_1010, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace('  ', (7990, 7992), self.input.position)
                _G_apply_1011, lastError = self._apply(self.rule_E, "E", [])
                self.considerError(lastError, None)
                self._trace('  |', (7992, 7995), self.input.position)
                _G_apply_1012, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace(" '['", (7995, 7999), self.input.position)
                _G_exactly_1013, lastError = self.exactly('(')
                self.considerError(lastError, None)
                self._trace('\n  ', (7999, 8002), self.input.position)
                _G_apply_1014, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('              (\n ', (8002, 8019), self.input.position)
                _G_apply_1015, lastError = self._apply(self.rule_FilterExpression, "FilterExpression", [])
                self.considerError(lastError, None)
                _locals['fex'] = _G_apply_1015
                self._trace('   ', (8023, 8026), self.input.position)
                _G_apply_1016, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('    ', (8026, 8030), self.input.position)
                _G_exactly_1017, lastError = self.exactly(')')
                self.considerError(lastError, None)
                _G_python_1019, lastError = eval(self._G_expr_1018, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_1019, self.currentError)
            def _G_or_1020():
                self._trace('ad', (8054, 8056), self.input.position)
                _G_apply_1021, lastError = self._apply(self.rule_S, "S", [])
                self.considerError(lastError, None)
                self._trace(' W', (8056, 8058), self.input.position)
                _G_apply_1022, lastError = self._apply(self.rule_I, "I", [])
                self.considerError(lastError, None)
                self._trace('S\n', (8058, 8060), self.input.position)
                _G_apply_1023, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace('  ', (8060, 8062), self.input.position)
                _G_apply_1024, lastError = self._apply(self.rule_G, "G", [])
                self.considerError(lastError, None)
                self._trace('  ', (8062, 8064), self.input.position)
                _G_apply_1025, lastError = self._apply(self.rule_L, "L", [])
                self.considerError(lastError, None)
                self._trace('  ', (8064, 8066), self.input.position)
                _G_apply_1026, lastError = self._apply(self.rule_E, "E", [])
                self.considerError(lastError, None)
                self._trace('   ', (8066, 8069), self.input.position)
                _G_apply_1027, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('    ', (8069, 8073), self.input.position)
                _G_exactly_1028, lastError = self.exactly('(')
                self.considerError(lastError, None)
                self._trace('   ', (8073, 8076), self.input.position)
                _G_apply_1029, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace("    (',' WS Expre", (8076, 8093), self.input.position)
                _G_apply_1030, lastError = self._apply(self.rule_FilterExpression, "FilterExpression", [])
                self.considerError(lastError, None)
                _locals['fex'] = _G_apply_1030
                self._trace('n:i', (8097, 8100), self.input.position)
                _G_apply_1031, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('tem ', (8100, 8104), self.input.position)
                _G_exactly_1032, lastError = self.exactly(')')
                self.considerError(lastError, None)
                _G_python_1034, lastError = eval(self._G_expr_1033, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_1034, self.currentError)
            def _G_or_1035():
                self._trace('     )*:tail -> [head', (8130, 8151), self.input.position)
                _G_apply_1036, lastError = self._apply(self.rule_RelationshipsPattern, "RelationshipsPattern", [])
                self.considerError(lastError, None)
                return (_G_apply_1036, self.currentError)
            def _G_or_1037():
                self._trace('l\n                    |\n  ', (8158, 8184), self.input.position)
                _G_apply_1038, lastError = self._apply(self.rule_GraphRelationshipsPattern, "GraphRelationshipsPattern", [])
                self.considerError(lastError, None)
                return (_G_apply_1038, self.currentError)
            def _G_or_1039():
                self._trace('           -> []\n       ', (8191, 8215), self.input.position)
                _G_apply_1040, lastError = self._apply(self.rule_parenthesizedExpression, "parenthesizedExpression", [])
                self.considerError(lastError, None)
                return (_G_apply_1040, self.currentError)
            def _G_or_1041():
                self._trace('  ):ex\n            ', (8222, 8241), self.input.position)
                _G_apply_1042, lastError = self._apply(self.rule_FunctionInvocation, "FunctionInvocation", [])
                self.considerError(lastError, None)
                return (_G_apply_1042, self.currentError)
            def _G_or_1043():
                self._trace('["List", ', (8248, 8257), self.input.position)
                _G_apply_1044, lastError = self._apply(self.rule_Variable, "Variable", [])
                self.considerError(lastError, None)
                return (_G_apply_1044, self.currentError)
            _G_or_1045, lastError = self._or([_G_or_884, _G_or_886, _G_or_888, _G_or_890, _G_or_896, _G_or_903, _G_or_909, _G_or_911, _G_or_921, _G_or_923, _G_or_925, _G_or_946, _G_or_961, _G_or_983, _G_or_995, _G_or_1007, _G_or_1020, _G_or_1035, _G_or_1037, _G_or_1039, _G_or_1041, _G_or_1043])
            self.considerError(lastError, 'Atom')
            return (_G_or_1045, self.currentError)


        def rule_parenthesizedExpression(self):
            _locals = {'self': self}
            self.locals['parenthesizedExpression'] = _locals
            self._trace("WS '", (8284, 8288), self.input.position)
            _G_exactly_1046, lastError = self.exactly('(')
            self.considerError(lastError, 'parenthesizedExpression')
            self._trace("(' ", (8288, 8291), self.input.position)
            _G_apply_1047, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'parenthesizedExpression')
            self._trace('WS FilterEx', (8291, 8302), self.input.position)
            _G_apply_1048, lastError = self._apply(self.rule_Expression, "Expression", [])
            self.considerError(lastError, 'parenthesizedExpression')
            _locals['ex'] = _G_apply_1048
            self._trace('ssi', (8305, 8308), self.input.position)
            _G_apply_1049, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'parenthesizedExpression')
            self._trace('on:f', (8308, 8312), self.input.position)
            _G_exactly_1050, lastError = self.exactly(')')
            self.considerError(lastError, 'parenthesizedExpression')
            _G_python_1052, lastError = eval(self._G_expr_1051, self.globals, _locals), None
            self.considerError(lastError, 'parenthesizedExpression')
            return (_G_python_1052, self.currentError)


        def rule_RelationshipsPattern(self):
            _locals = {'self': self}
            self.locals['RelationshipsPattern'] = _locals
            self._trace('        | E ', (8342, 8354), self.input.position)
            _G_apply_1053, lastError = self._apply(self.rule_NodePattern, "NodePattern", [])
            self.considerError(lastError, 'RelationshipsPattern')
            _locals['np'] = _G_apply_1053
            def _G_optional_1054():
                self._trace(' A', (8359, 8361), self.input.position)
                _G_apply_1055, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace(" C T WS '(' WS Filte", (8361, 8381), self.input.position)
                _G_apply_1056, lastError = self._apply(self.rule_PatternElementChain, "PatternElementChain", [])
                self.considerError(lastError, None)
                return (_G_apply_1056, self.currentError)
            def _G_optional_1057():
                return (None, self.input.nullError())
            _G_or_1058, lastError = self._or([_G_optional_1054, _G_optional_1057])
            self.considerError(lastError, 'RelationshipsPattern')
            _locals['pec'] = _G_or_1058
            _G_python_1060, lastError = eval(self._G_expr_1059, self.globals, _locals), None
            self.considerError(lastError, 'RelationshipsPattern')
            return (_G_python_1060, self.currentError)


        def rule_GraphRelationshipsPattern(self):
            _locals = {'self': self}
            self.locals['GraphRelationshipsPattern'] = _locals
            self._trace('        |', (8453, 8462), self.input.position)
            _G_apply_1061, lastError = self._apply(self.rule_Variable, "Variable", [])
            self.considerError(lastError, 'GraphRelationshipsPattern')
            _locals['v'] = _G_apply_1061
            self._trace(' L L', (8464, 8468), self.input.position)
            _G_exactly_1062, lastError = self.exactly(':')
            self.considerError(lastError, 'GraphRelationshipsPattern')
            self._trace(' WS', (8468, 8471), self.input.position)
            _G_apply_1063, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'GraphRelationshipsPattern')
            self._trace(" '(' WS Filt", (8471, 8483), self.input.position)
            _G_apply_1064, lastError = self._apply(self.rule_NodePattern, "NodePattern", [])
            self.considerError(lastError, 'GraphRelationshipsPattern')
            _locals['np'] = _G_apply_1064
            def _G_optional_1065():
                self._trace('re', (8488, 8490), self.input.position)
                _G_apply_1066, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace("ssion:fex WS ')' -> ", (8490, 8510), self.input.position)
                _G_apply_1067, lastError = self._apply(self.rule_PatternElementChain, "PatternElementChain", [])
                self.considerError(lastError, None)
                return (_G_apply_1067, self.currentError)
            def _G_optional_1068():
                return (None, self.input.nullError())
            _G_or_1069, lastError = self._or([_G_optional_1065, _G_optional_1068])
            self.considerError(lastError, 'GraphRelationshipsPattern')
            _locals['pec'] = _G_or_1069
            _G_python_1071, lastError = eval(self._G_expr_1070, self.globals, _locals), None
            self.considerError(lastError, 'GraphRelationshipsPattern')
            return (_G_python_1071, self.currentError)


        def rule_FilterExpression(self):
            _locals = {'self': self}
            self.locals['FilterExpression'] = _locals
            self._trace('["Any", f', (8581, 8590), self.input.position)
            _G_apply_1072, lastError = self._apply(self.rule_IdInColl, "IdInColl", [])
            self.considerError(lastError, 'FilterExpression')
            _locals['i'] = _G_apply_1072
            def _G_optional_1073():
                self._trace('  ', (8594, 8596), self.input.position)
                _G_apply_1074, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('      ', (8596, 8602), self.input.position)
                _G_apply_1075, lastError = self._apply(self.rule_Where, "Where", [])
                self.considerError(lastError, None)
                return (_G_apply_1075, self.currentError)
            def _G_optional_1076():
                return (None, self.input.nullError())
            _G_or_1077, lastError = self._or([_G_optional_1073, _G_optional_1076])
            self.considerError(lastError, 'FilterExpression')
            _locals['w'] = _G_or_1077
            _G_python_1079, lastError = eval(self._G_expr_1078, self.globals, _locals), None
            self.considerError(lastError, 'FilterExpression')
            return (_G_python_1079, self.currentError)


        def rule_IdInColl(self):
            _locals = {'self': self}
            self.locals['IdInColl'] = _locals
            self._trace(')\' -> ["N', (8648, 8657), self.input.position)
            _G_apply_1080, lastError = self._apply(self.rule_Variable, "Variable", [])
            self.considerError(lastError, 'IdInColl')
            _locals['v'] = _G_apply_1080
            self._trace('e",', (8659, 8662), self.input.position)
            _G_apply_1081, lastError = self._apply(self.rule_SP, "SP", [])
            self.considerError(lastError, 'IdInColl')
            self._trace(' f', (8662, 8664), self.input.position)
            _G_apply_1082, lastError = self._apply(self.rule_I, "I", [])
            self.considerError(lastError, 'IdInColl')
            self._trace('ex', (8664, 8666), self.input.position)
            _G_apply_1083, lastError = self._apply(self.rule_N, "N", [])
            self.considerError(lastError, 'IdInColl')
            self._trace(']\n ', (8666, 8669), self.input.position)
            _G_apply_1084, lastError = self._apply(self.rule_SP, "SP", [])
            self.considerError(lastError, 'IdInColl')
            self._trace('        | S', (8669, 8680), self.input.position)
            _G_apply_1085, lastError = self._apply(self.rule_Expression, "Expression", [])
            self.considerError(lastError, 'IdInColl')
            _locals['ex'] = _G_apply_1085
            _G_python_1087, lastError = eval(self._G_expr_1086, self.globals, _locals), None
            self.considerError(lastError, 'IdInColl')
            return (_G_python_1087, self.currentError)


        def rule_FunctionInvocation(self):
            _locals = {'self': self}
            self.locals['FunctionInvocation'] = _locals
            self._trace(' -> ["Single"', (8728, 8741), self.input.position)
            _G_apply_1088, lastError = self._apply(self.rule_FunctionName, "FunctionName", [])
            self.considerError(lastError, 'FunctionInvocation')
            _locals['func'] = _G_apply_1088
            self._trace(']\n         | Relationsh', (8746, 8769), self.input.position)
            _G_apply_1089, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'FunctionInvocation')
            self._trace('ipsP', (8769, 8773), self.input.position)
            _G_exactly_1090, lastError = self.exactly('(')
            self.considerError(lastError, 'FunctionInvocation')
            self._trace('att', (8773, 8776), self.input.position)
            _G_apply_1091, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'FunctionInvocation')
            def _G_optional_1092():
                self._trace('l', (8798, 8799), self.input.position)
                _G_apply_1093, lastError = self._apply(self.rule_D, "D", [])
                self.considerError(lastError, None)
                self._trace('at', (8799, 8801), self.input.position)
                _G_apply_1094, lastError = self._apply(self.rule_I, "I", [])
                self.considerError(lastError, None)
                self._trace('io', (8801, 8803), self.input.position)
                _G_apply_1095, lastError = self._apply(self.rule_S, "S", [])
                self.considerError(lastError, None)
                self._trace('ns', (8803, 8805), self.input.position)
                _G_apply_1096, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                self._trace('hi', (8805, 8807), self.input.position)
                _G_apply_1097, lastError = self._apply(self.rule_I, "I", [])
                self.considerError(lastError, None)
                self._trace('ps', (8807, 8809), self.input.position)
                _G_apply_1098, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                self._trace('Pa', (8809, 8811), self.input.position)
                _G_apply_1099, lastError = self._apply(self.rule_C, "C", [])
                self.considerError(lastError, None)
                self._trace('tt', (8811, 8813), self.input.position)
                _G_apply_1100, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                self._trace('ern', (8813, 8816), self.input.position)
                _G_apply_1101, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                _G_python_1102, lastError = ("distinct"), None
                self.considerError(lastError, None)
                return (_G_python_1102, self.currentError)
            def _G_optional_1103():
                return (None, self.input.nullError())
            _G_or_1104, lastError = self._or([_G_optional_1092, _G_optional_1103])
            self.considerError(lastError, 'FunctionInvocation')
            _locals['distinct'] = _G_or_1104
            def _G_or_1105():
                self._trace('FunctionInvocation\n         | Varia', (8863, 8898), self.input.position)
                _G_apply_1106, lastError = self._apply(self.rule_Expression, "Expression", [])
                self.considerError(lastError, None)
                _locals['head'] = _G_apply_1106
                def _G_many_1107():
                    self._trace("n = '(' WS Expression:ex WS ')' ", (8929, 8961), self.input.position)
                    _G_exactly_1108, lastError = self.exactly(',')
                    self.considerError(lastError, None)
                    self._trace('-> ', (8961, 8964), self.input.position)
                    _G_apply_1109, lastError = self._apply(self.rule_WS, "WS", [])
                    self.considerError(lastError, None)
                    self._trace('ex\n\n    Rel', (8964, 8975), self.input.position)
                    _G_apply_1110, lastError = self._apply(self.rule_Expression, "Expression", [])
                    self.considerError(lastError, None)
                    return (_G_apply_1110, self.currentError)
                _G_many_1111, lastError = self.many(_G_many_1107)
                self.considerError(lastError, None)
                _locals['tail'] = _G_many_1111
                _G_python_1112, lastError = eval(self._G_expr_424, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_1112, self.currentError)
            def _G_or_1113():
                _G_python_1114, lastError = ([]), None
                self.considerError(lastError, None)
                return (_G_python_1114, self.currentError)
            _G_or_1115, lastError = self._or([_G_or_1105, _G_or_1113])
            self.considerError(lastError, 'FunctionInvocation')
            _locals['args'] = _G_or_1115
            self._trace('  \n    GraphRelationshi', (9079, 9102), self.input.position)
            _G_apply_1116, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'FunctionInvocation')
            self._trace('psPa', (9102, 9106), self.input.position)
            _G_exactly_1117, lastError = self.exactly(')')
            self.considerError(lastError, 'FunctionInvocation')
            _G_python_1119, lastError = eval(self._G_expr_1118, self.globals, _locals), None
            self.considerError(lastError, 'FunctionInvocation')
            return (_G_python_1119, self.currentError)


        def rule_FunctionName(self):
            _locals = {'self': self}
            self.locals['FunctionName'] = _locals
            self._trace('rnElementChai', (9156, 9169), self.input.position)
            _G_apply_1120, lastError = self._apply(self.rule_SymbolicName, "SymbolicName", [])
            self.considerError(lastError, 'FunctionName')
            return (_G_apply_1120, self.currentError)


        def rule_ListComprehension(self):
            _locals = {'self': self}
            self.locals['ListComprehension'] = _locals
            self._trace('atio', (9190, 9194), self.input.position)
            _G_exactly_1121, lastError = self.exactly('[')
            self.considerError(lastError, 'ListComprehension')
            self._trace('nshipsPattern", v', (9194, 9211), self.input.position)
            _G_apply_1122, lastError = self._apply(self.rule_FilterExpression, "FilterExpression", [])
            self.considerError(lastError, 'ListComprehension')
            _locals['fex'] = _G_apply_1122
            def _G_optional_1123():
                self._trace('pe', (9217, 9219), self.input.position)
                _G_apply_1124, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('c]\n\n', (9219, 9223), self.input.position)
                _G_exactly_1125, lastError = self.exactly('|')
                self.considerError(lastError, None)
                self._trace('    FilterE', (9223, 9234), self.input.position)
                _G_apply_1126, lastError = self._apply(self.rule_Expression, "Expression", [])
                self.considerError(lastError, None)
                return (_G_apply_1126, self.currentError)
            def _G_optional_1127():
                return (None, self.input.nullError())
            _G_or_1128, lastError = self._or([_G_optional_1123, _G_optional_1127])
            self.considerError(lastError, 'ListComprehension')
            _locals['ex'] = _G_or_1128
            self._trace('sion', (9239, 9243), self.input.position)
            _G_exactly_1129, lastError = self.exactly(']')
            self.considerError(lastError, 'ListComprehension')
            _G_python_1131, lastError = eval(self._G_expr_1130, self.globals, _locals), None
            self.considerError(lastError, 'ListComprehension')
            return (_G_python_1131, self.currentError)


        def rule_PropertyLookup(self):
            _locals = {'self': self}
            self.locals['PropertyLookup'] = _locals
            self._trace('\n\n ', (9374, 9377), self.input.position)
            _G_apply_1132, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'PropertyLookup')
            self._trace('   F', (9377, 9381), self.input.position)
            _G_exactly_1133, lastError = self.exactly('.')
            self.considerError(lastError, 'PropertyLookup')
            self._trace('unc', (9381, 9384), self.input.position)
            _G_apply_1134, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'PropertyLookup')
            self._trace('tionInvocation =', (9384, 9400), self.input.position)
            _G_apply_1135, lastError = self._apply(self.rule_PropertyKeyName, "PropertyKeyName", [])
            self.considerError(lastError, 'PropertyLookup')
            _locals['n'] = _G_apply_1135
            _G_python_1137, lastError = eval(self._G_expr_1136, self.globals, _locals), None
            self.considerError(lastError, 'PropertyLookup')
            return (_G_python_1137, self.currentError)


        def rule_CaseExpression(self):
            _locals = {'self': self}
            self.locals['CaseExpression'] = _locals
            self._trace(" '(' WS\n           ", (9445, 9464), self.input.position)
            _G_apply_1138, lastError = self._apply(self.rule_C, "C", [])
            self.considerError(lastError, 'CaseExpression')
            self._trace('  ', (9464, 9466), self.input.position)
            _G_apply_1139, lastError = self._apply(self.rule_A, "A", [])
            self.considerError(lastError, 'CaseExpression')
            self._trace('  ', (9466, 9468), self.input.position)
            _G_apply_1140, lastError = self._apply(self.rule_S, "S", [])
            self.considerError(lastError, 'CaseExpression')
            self._trace('  ', (9468, 9470), self.input.position)
            _G_apply_1141, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'CaseExpression')
            self._trace('   ', (9470, 9473), self.input.position)
            _G_apply_1142, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'CaseExpression')
            def _G_optional_1143():
                self._trace('T WS -> "d', (9492, 9502), self.input.position)
                _G_apply_1144, lastError = self._apply(self.rule_Expression, "Expression", [])
                self.considerError(lastError, None)
                return (_G_apply_1144, self.currentError)
            def _G_optional_1145():
                return (None, self.input.nullError())
            _G_or_1146, lastError = self._or([_G_optional_1143, _G_optional_1145])
            self.considerError(lastError, 'CaseExpression')
            _locals['ex'] = _G_or_1146
            def _G_many1_1147():
                self._trace('  ', (9526, 9528), self.input.position)
                _G_apply_1148, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('                 ', (9528, 9545), self.input.position)
                _G_apply_1149, lastError = self._apply(self.rule_CaseAlternatives, "CaseAlternatives", [])
                self.considerError(lastError, None)
                return (_G_apply_1149, self.currentError)
            _G_many1_1150, lastError = self.many(_G_many1_1147, _G_many1_1147())
            self.considerError(lastError, 'CaseExpression')
            _locals['cas'] = _G_many1_1150
            def _G_optional_1151():
                self._trace('  ', (9571, 9573), self.input.position)
                _G_apply_1152, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('  ', (9573, 9575), self.input.position)
                _G_apply_1153, lastError = self._apply(self.rule_E, "E", [])
                self.considerError(lastError, None)
                self._trace(' E', (9575, 9577), self.input.position)
                _G_apply_1154, lastError = self._apply(self.rule_L, "L", [])
                self.considerError(lastError, None)
                self._trace('xp', (9577, 9579), self.input.position)
                _G_apply_1155, lastError = self._apply(self.rule_S, "S", [])
                self.considerError(lastError, None)
                self._trace('re', (9579, 9581), self.input.position)
                _G_apply_1156, lastError = self._apply(self.rule_E, "E", [])
                self.considerError(lastError, None)
                self._trace('ssi', (9581, 9584), self.input.position)
                _G_apply_1157, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('on:head\n   ', (9584, 9595), self.input.position)
                _G_apply_1158, lastError = self._apply(self.rule_Expression, "Expression", [])
                self.considerError(lastError, None)
                return (_G_apply_1158, self.currentError)
            def _G_optional_1159():
                return (None, self.input.nullError())
            _G_or_1160, lastError = self._or([_G_optional_1151, _G_optional_1159])
            self.considerError(lastError, 'CaseExpression')
            _locals['el'] = _G_or_1160
            self._trace('                    ', (9600, 9620), self.input.position)
            _G_apply_1161, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'CaseExpression')
            self._trace('(\n', (9620, 9622), self.input.position)
            _G_apply_1162, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'CaseExpression')
            self._trace('  ', (9622, 9624), self.input.position)
            _G_apply_1163, lastError = self._apply(self.rule_N, "N", [])
            self.considerError(lastError, 'CaseExpression')
            self._trace('  ', (9624, 9626), self.input.position)
            _G_apply_1164, lastError = self._apply(self.rule_D, "D", [])
            self.considerError(lastError, 'CaseExpression')
            _G_python_1166, lastError = eval(self._G_expr_1165, self.globals, _locals), None
            self.considerError(lastError, 'CaseExpression')
            return (_G_python_1166, self.currentError)


        def rule_CaseAlternatives(self):
            _locals = {'self': self}
            self.locals['CaseAlternatives'] = _locals
            self._trace('  ', (9688, 9690), self.input.position)
            _G_apply_1167, lastError = self._apply(self.rule_W, "W", [])
            self.considerError(lastError, 'CaseAlternatives')
            self._trace('  ', (9690, 9692), self.input.position)
            _G_apply_1168, lastError = self._apply(self.rule_H, "H", [])
            self.considerError(lastError, 'CaseAlternatives')
            self._trace('  ', (9692, 9694), self.input.position)
            _G_apply_1169, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'CaseAlternatives')
            self._trace('  ', (9694, 9696), self.input.position)
            _G_apply_1170, lastError = self._apply(self.rule_N, "N", [])
            self.considerError(lastError, 'CaseAlternatives')
            self._trace('   ', (9696, 9699), self.input.position)
            _G_apply_1171, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'CaseAlternatives')
            self._trace(' )*:tail ->', (9699, 9710), self.input.position)
            _G_apply_1172, lastError = self._apply(self.rule_Expression, "Expression", [])
            self.considerError(lastError, 'CaseAlternatives')
            _locals['ex1'] = _G_apply_1172
            self._trace('ad]', (9714, 9717), self.input.position)
            _G_apply_1173, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'CaseAlternatives')
            self._trace(' +', (9717, 9719), self.input.position)
            _G_apply_1174, lastError = self._apply(self.rule_T, "T", [])
            self.considerError(lastError, 'CaseAlternatives')
            self._trace(' t', (9719, 9721), self.input.position)
            _G_apply_1175, lastError = self._apply(self.rule_H, "H", [])
            self.considerError(lastError, 'CaseAlternatives')
            self._trace('ai', (9721, 9723), self.input.position)
            _G_apply_1176, lastError = self._apply(self.rule_E, "E", [])
            self.considerError(lastError, 'CaseAlternatives')
            self._trace('l\n', (9723, 9725), self.input.position)
            _G_apply_1177, lastError = self._apply(self.rule_N, "N", [])
            self.considerError(lastError, 'CaseAlternatives')
            self._trace('   ', (9725, 9728), self.input.position)
            _G_apply_1178, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'CaseAlternatives')
            self._trace('           ', (9728, 9739), self.input.position)
            _G_apply_1179, lastError = self._apply(self.rule_Expression, "Expression", [])
            self.considerError(lastError, 'CaseAlternatives')
            _locals['ex2'] = _G_apply_1179
            _G_python_1181, lastError = eval(self._G_expr_1180, self.globals, _locals), None
            self.considerError(lastError, 'CaseAlternatives')
            return (_G_python_1181, self.currentError)


        def rule_Variable(self):
            _locals = {'self': self}
            self.locals['Variable'] = _locals
            self._trace('            )', (9769, 9782), self.input.position)
            _G_apply_1182, lastError = self._apply(self.rule_SymbolicName, "SymbolicName", [])
            self.considerError(lastError, 'Variable')
            _locals['s'] = _G_apply_1182
            _G_python_1184, lastError = eval(self._G_expr_1183, self.globals, _locals), None
            self.considerError(lastError, 'Variable')
            return (_G_python_1184, self.currentError)


        def rule_StringLiteral(self):
            _locals = {'self': self}
            self.locals['StringLiteral'] = _locals
            def _G_or_1185():
                self._trace('["call", func, dis', (9822, 9840), self.input.position)
                _G_exactly_1186, lastError = self.exactly('"')
                self.considerError(lastError, None)
                def _G_many_1187():
                    def _G_or_1188():
                        def _G_not_1189():
                            def _G_or_1190():
                                self._trace('t, ', (9844, 9847), self.input.position)
                                _G_exactly_1191, lastError = self.exactly('"')
                                self.considerError(lastError, None)
                                return (_G_exactly_1191, self.currentError)
                            def _G_or_1192():
                                self._trace('rgs]', (9848, 9852), self.input.position)
                                _G_exactly_1193, lastError = self.exactly('\\')
                                self.considerError(lastError, None)
                                return (_G_exactly_1193, self.currentError)
                            _G_or_1194, lastError = self._or([_G_or_1190, _G_or_1192])
                            self.considerError(lastError, None)
                            return (_G_or_1194, self.currentError)
                        _G_not_1195, lastError = self._not(_G_not_1189)
                        self.considerError(lastError, None)
                        self._trace('\n    Func', (9853, 9862), self.input.position)
                        _G_apply_1196, lastError = self._apply(self.rule_anything, "anything", [])
                        self.considerError(lastError, None)
                        return (_G_apply_1196, self.currentError)
                    def _G_or_1197():
                        self._trace('onName = Sym', (9864, 9876), self.input.position)
                        _G_apply_1198, lastError = self._apply(self.rule_EscapedChar, "EscapedChar", [])
                        self.considerError(lastError, None)
                        return (_G_apply_1198, self.currentError)
                    _G_or_1199, lastError = self._or([_G_or_1188, _G_or_1197])
                    self.considerError(lastError, None)
                    return (_G_or_1199, self.currentError)
                _G_many_1200, lastError = self.many(_G_many_1187)
                self.considerError(lastError, None)
                _locals['cs'] = _G_many_1200
                self._trace('Name', (9881, 9885), self.input.position)
                _G_exactly_1201, lastError = self.exactly('"')
                self.considerError(lastError, None)
                _G_python_1203, lastError = eval(self._G_expr_1202, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_1203, self.currentError)
            def _G_or_1204():
                self._trace('ilte', (9916, 9920), self.input.position)
                _G_apply_1205, lastError = self._apply(self.rule_token, "token", ["'"])
                self.considerError(lastError, None)
                def _G_many_1206():
                    def _G_or_1207():
                        def _G_not_1208():
                            def _G_or_1209():
                                self._trace('res', (9924, 9927), self.input.position)
                                _G_apply_1210, lastError = self._apply(self.rule_token, "token", ["'"])
                                self.considerError(lastError, None)
                                return (_G_apply_1210, self.currentError)
                            def _G_or_1211():
                                self._trace('ion:', (9928, 9932), self.input.position)
                                _G_exactly_1212, lastError = self.exactly('\\')
                                self.considerError(lastError, None)
                                return (_G_exactly_1212, self.currentError)
                            _G_or_1213, lastError = self._or([_G_or_1209, _G_or_1211])
                            self.considerError(lastError, None)
                            return (_G_or_1213, self.currentError)
                        _G_not_1214, lastError = self._not(_G_not_1208)
                        self.considerError(lastError, None)
                        self._trace("ex (WS '|", (9933, 9942), self.input.position)
                        _G_apply_1215, lastError = self._apply(self.rule_anything, "anything", [])
                        self.considerError(lastError, None)
                        return (_G_apply_1215, self.currentError)
                    def _G_or_1216():
                        self._trace('Expression)?', (9944, 9956), self.input.position)
                        _G_apply_1217, lastError = self._apply(self.rule_EscapedChar, "EscapedChar", [])
                        self.considerError(lastError, None)
                        return (_G_apply_1217, self.currentError)
                    _G_or_1218, lastError = self._or([_G_or_1207, _G_or_1216])
                    self.considerError(lastError, None)
                    return (_G_or_1218, self.currentError)
                _G_many_1219, lastError = self.many(_G_many_1206)
                self.considerError(lastError, None)
                _locals['cs'] = _G_many_1219
                self._trace("]' -", (9961, 9965), self.input.position)
                _G_apply_1220, lastError = self._apply(self.rule_token, "token", ["'"])
                self.considerError(lastError, None)
                _G_python_1221, lastError = eval(self._G_expr_1202, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_1221, self.currentError)
            _G_or_1222, lastError = self._or([_G_or_1185, _G_or_1204])
            self.considerError(lastError, 'StringLiteral')
            _locals['l'] = _G_or_1222
            _G_python_1224, lastError = eval(self._G_expr_1223, self.globals, _locals), None
            self.considerError(lastError, 'StringLiteral')
            return (_G_python_1224, self.currentError)


        def rule_EscapedChar(self):
            _locals = {'self': self}
            self.locals['EscapedChar'] = _locals
            self._trace(' ((Pr', (10031, 10036), self.input.position)
            _G_exactly_1225, lastError = self.exactly('\\')
            self.considerError(lastError, 'EscapedChar')
            def _G_or_1226():
                self._trace("('?'", (10050, 10054), self.input.position)
                _G_exactly_1227, lastError = self.exactly('\\')
                self.considerError(lastError, None)
                _G_python_1228, lastError = ('\\'), None
                self.considerError(lastError, None)
                return (_G_python_1228, self.currentError)
            def _G_or_1229():
                self._trace('Name', (10076, 10080), self.input.position)
                _G_apply_1230, lastError = self._apply(self.rule_token, "token", ["'"])
                self.considerError(lastError, None)
                _G_python_1231, lastError = ("'"), None
                self.considerError(lastError, None)
                return (_G_python_1231, self.currentError)
            def _G_or_1232():
                self._trace('= WS', (10101, 10105), self.input.position)
                _G_exactly_1233, lastError = self.exactly('"')
                self.considerError(lastError, None)
                _G_python_1234, lastError = ('"'), None
                self.considerError(lastError, None)
                return (_G_python_1234, self.currentError)
            def _G_or_1235():
                self._trace('me', (10126, 10128), self.input.position)
                _G_apply_1236, lastError = self._apply(self.rule_N, "N", [])
                self.considerError(lastError, None)
                _G_python_1237, lastError = ('\n'), None
                self.considerError(lastError, None)
                return (_G_python_1237, self.currentError)
            def _G_or_1238():
                self._trace('",', (10150, 10152), self.input.position)
                _G_apply_1239, lastError = self._apply(self.rule_R, "R", [])
                self.considerError(lastError, None)
                _G_python_1240, lastError = ('\r'), None
                self.considerError(lastError, None)
                return (_G_python_1240, self.currentError)
            def _G_or_1241():
                self._trace('n ', (10174, 10176), self.input.position)
                _G_apply_1242, lastError = self._apply(self.rule_T, "T", [])
                self.considerError(lastError, None)
                _G_python_1243, lastError = ('\t'), None
                self.considerError(lastError, None)
                return (_G_python_1243, self.currentError)
            def _G_or_1244():
                self._trace(' C A', (10198, 10202), self.input.position)
                _G_exactly_1245, lastError = self.exactly('_')
                self.considerError(lastError, None)
                _G_python_1246, lastError = ('_'), None
                self.considerError(lastError, None)
                return (_G_python_1246, self.currentError)
            def _G_or_1247():
                self._trace('    ', (10223, 10227), self.input.position)
                _G_exactly_1248, lastError = self.exactly('%')
                self.considerError(lastError, None)
                _G_python_1249, lastError = ('%'), None
                self.considerError(lastError, None)
                return (_G_python_1249, self.currentError)
            _G_or_1250, lastError = self._or([_G_or_1226, _G_or_1229, _G_or_1232, _G_or_1235, _G_or_1238, _G_or_1241, _G_or_1244, _G_or_1247])
            self.considerError(lastError, 'EscapedChar')
            return (_G_or_1250, self.currentError)


        def rule_NumberLiteral(self):
            _locals = {'self': self}
            self.locals['NumberLiteral'] = _locals
            def _G_or_1251():
                self._trace('  (WS CaseAlternatives)+:cas', (10267, 10295), self.input.position)
                _G_apply_1252, lastError = self._apply(self.rule_DoubleLiteral, "DoubleLiteral", [])
                self.considerError(lastError, None)
                return (_G_apply_1252, self.currentError)
            def _G_or_1253():
                self._trace('       (WS E L ', (10311, 10326), self.input.position)
                _G_apply_1254, lastError = self._apply(self.rule_IntegerLiteral, "IntegerLiteral", [])
                self.considerError(lastError, None)
                return (_G_apply_1254, self.currentError)
            _G_or_1255, lastError = self._or([_G_or_1251, _G_or_1253])
            self.considerError(lastError, 'NumberLiteral')
            _locals['l'] = _G_or_1255
            _G_python_1256, lastError = eval(self._G_expr_1223, self.globals, _locals), None
            self.considerError(lastError, 'NumberLiteral')
            return (_G_python_1256, self.currentError)


        def rule_MapLiteral(self):
            _locals = {'self': self}
            self.locals['MapLiteral'] = _locals
            self._trace(' D\n ', (10376, 10380), self.input.position)
            _G_exactly_1257, lastError = self.exactly('{')
            self.considerError(lastError, 'MapLiteral')
            self._trace('   ', (10380, 10383), self.input.position)
            _G_apply_1258, lastError = self._apply(self.rule_WS, "WS", [])
            self.considerError(lastError, 'MapLiteral')
            def _G_or_1259():
                self._trace('cas, el]\n\n    CaseAlternatives = W H', (10416, 10452), self.input.position)
                _G_apply_1260, lastError = self._apply(self.rule_PropertyKeyName, "PropertyKeyName", [])
                self.considerError(lastError, None)
                _locals['k'] = _G_apply_1260
                self._trace(' N ', (10454, 10457), self.input.position)
                _G_apply_1261, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('WS E', (10457, 10461), self.input.position)
                _G_exactly_1262, lastError = self.exactly(':')
                self.considerError(lastError, None)
                self._trace('xpr', (10461, 10464), self.input.position)
                _G_apply_1263, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace('ession:ex1 ', (10464, 10475), self.input.position)
                _G_apply_1264, lastError = self._apply(self.rule_Expression, "Expression", [])
                self.considerError(lastError, None)
                _locals['v'] = _G_apply_1264
                _G_python_1266, lastError = eval(self._G_expr_1265, self.globals, _locals), None
                self.considerError(lastError, None)
                _locals['head'] = _G_python_1266
                self._trace('1, ', (10510, 10513), self.input.position)
                _G_apply_1267, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                def _G_many_1268():
                    self._trace(' = SymbolicName:s -> ["V', (10531, 10555), self.input.position)
                    _G_exactly_1269, lastError = self.exactly(',')
                    self.considerError(lastError, None)
                    self._trace('ari', (10555, 10558), self.input.position)
                    _G_apply_1270, lastError = self._apply(self.rule_WS, "WS", [])
                    self.considerError(lastError, None)
                    self._trace('able", s]\n\n    S', (10558, 10574), self.input.position)
                    _G_apply_1271, lastError = self._apply(self.rule_PropertyKeyName, "PropertyKeyName", [])
                    self.considerError(lastError, None)
                    _locals['k'] = _G_apply_1271
                    self._trace('ing', (10576, 10579), self.input.position)
                    _G_apply_1272, lastError = self._apply(self.rule_WS, "WS", [])
                    self.considerError(lastError, None)
                    self._trace('Lite', (10579, 10583), self.input.position)
                    _G_exactly_1273, lastError = self.exactly(':')
                    self.considerError(lastError, None)
                    self._trace('ral', (10583, 10586), self.input.position)
                    _G_apply_1274, lastError = self._apply(self.rule_WS, "WS", [])
                    self.considerError(lastError, None)
                    self._trace(' = (\n      ', (10586, 10597), self.input.position)
                    _G_apply_1275, lastError = self._apply(self.rule_Expression, "Expression", [])
                    self.considerError(lastError, None)
                    _locals['v'] = _G_apply_1275
                    self._trace('   ', (10599, 10602), self.input.position)
                    _G_apply_1276, lastError = self._apply(self.rule_WS, "WS", [])
                    self.considerError(lastError, None)
                    _G_python_1277, lastError = eval(self._G_expr_1265, self.globals, _locals), None
                    self.considerError(lastError, None)
                    return (_G_python_1277, self.currentError)
                _G_many_1278, lastError = self.many(_G_many_1268)
                self.considerError(lastError, None)
                _locals['tail'] = _G_many_1278
                _G_python_1279, lastError = eval(self._G_expr_424, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_1279, self.currentError)
            def _G_or_1280():
                _G_python_1281, lastError = ([]), None
                self.considerError(lastError, None)
                return (_G_python_1281, self.currentError)
            _G_or_1282, lastError = self._or([_G_or_1259, _G_or_1280])
            self.considerError(lastError, 'MapLiteral')
            _locals['pairs'] = _G_or_1282
            self._trace('          | "\'" ', (10681, 10697), self.input.position)
            _G_exactly_1283, lastError = self.exactly('}')
            self.considerError(lastError, 'MapLiteral')
            _G_python_1285, lastError = eval(self._G_expr_1284, self.globals, _locals), None
            self.considerError(lastError, 'MapLiteral')
            return (_G_python_1285, self.currentError)


        def rule_Parameter(self):
            _locals = {'self': self}
            self.locals['Parameter'] = _locals
            self._trace('"\'" ', (10738, 10742), self.input.position)
            _G_exactly_1286, lastError = self.exactly('$')
            self.considerError(lastError, 'Parameter')
            def _G_or_1287():
                self._trace(' "".join(cs)', (10744, 10756), self.input.position)
                _G_apply_1288, lastError = self._apply(self.rule_SymbolicName, "SymbolicName", [])
                self.considerError(lastError, None)
                return (_G_apply_1288, self.currentError)
            def _G_or_1289():
                self._trace('               ', (10758, 10773), self.input.position)
                _G_apply_1290, lastError = self._apply(self.rule_DecimalInteger, "DecimalInteger", [])
                self.considerError(lastError, None)
                return (_G_apply_1290, self.currentError)
            _G_or_1291, lastError = self._or([_G_or_1287, _G_or_1289])
            self.considerError(lastError, 'Parameter')
            _locals['p'] = _G_or_1291
            _G_python_1293, lastError = eval(self._G_expr_1292, self.globals, _locals), None
            self.considerError(lastError, 'Parameter')
            return (_G_python_1293, self.currentError)


        def rule_PropertyExpression(self):
            _locals = {'self': self}
            self.locals['PropertyExpression'] = _locals
            self._trace("\\'\n  ", (10818, 10823), self.input.position)
            _G_apply_1294, lastError = self._apply(self.rule_Atom, "Atom", [])
            self.considerError(lastError, 'PropertyExpression')
            _locals['a'] = _G_apply_1294
            def _G_many_1295():
                self._trace('  ', (10827, 10829), self.input.position)
                _G_apply_1296, lastError = self._apply(self.rule_WS, "WS", [])
                self.considerError(lastError, None)
                self._trace("        ('\\\\' -", (10829, 10844), self.input.position)
                _G_apply_1297, lastError = self._apply(self.rule_PropertyLookup, "PropertyLookup", [])
                self.considerError(lastError, None)
                return (_G_apply_1297, self.currentError)
            _G_many_1298, lastError = self.many(_G_many_1295)
            self.considerError(lastError, 'PropertyExpression')
            _locals['opts'] = _G_many_1298
            _G_python_1300, lastError = eval(self._G_expr_1299, self.globals, _locals), None
            self.considerError(lastError, 'PropertyExpression')
            return (_G_python_1300, self.currentError)


        def rule_PropertyKeyName(self):
            _locals = {'self': self}
            self.locals['PropertyKeyName'] = _locals
            self._trace(' \'"\' -> \'"\'\n ', (10897, 10910), self.input.position)
            _G_apply_1301, lastError = self._apply(self.rule_SymbolicName, "SymbolicName", [])
            self.considerError(lastError, 'PropertyKeyName')
            return (_G_apply_1301, self.currentError)


        def rule_IntegerLiteral(self):
            _locals = {'self': self}
            self.locals['IntegerLiteral'] = _locals
            def _G_or_1302():
                self._trace(" -> '\\n'\n  ", (10928, 10939), self.input.position)
                _G_apply_1303, lastError = self._apply(self.rule_HexInteger, "HexInteger", [])
                self.considerError(lastError, None)
                return (_G_apply_1303, self.currentError)
            def _G_or_1304():
                self._trace(" -> '\\r'\n    ", (10956, 10969), self.input.position)
                _G_apply_1305, lastError = self._apply(self.rule_OctalInteger, "OctalInteger", [])
                self.considerError(lastError, None)
                return (_G_apply_1305, self.currentError)
            def _G_or_1306():
                self._trace("> '\\t'\n        ", (10986, 11001), self.input.position)
                _G_apply_1307, lastError = self._apply(self.rule_DecimalInteger, "DecimalInteger", [])
                self.considerError(lastError, None)
                return (_G_apply_1307, self.currentError)
            _G_or_1308, lastError = self._or([_G_or_1302, _G_or_1304, _G_or_1306])
            self.considerError(lastError, 'IntegerLiteral')
            return (_G_or_1308, self.currentError)


        def rule_OctalDigit(self):
            _locals = {'self': self}
            self.locals['OctalDigit'] = _locals
            def _G_not_1309():
                def _G_or_1310():
                    self._trace("'_'", (11018, 11021), self.input.position)
                    _G_exactly_1311, lastError = self.exactly('8')
                    self.considerError(lastError, None)
                    return (_G_exactly_1311, self.currentError)
                def _G_or_1312():
                    self._trace('   ', (11022, 11025), self.input.position)
                    _G_exactly_1313, lastError = self.exactly('9')
                    self.considerError(lastError, None)
                    return (_G_exactly_1313, self.currentError)
                _G_or_1314, lastError = self._or([_G_or_1310, _G_or_1312])
                self.considerError(lastError, None)
                return (_G_or_1314, self.currentError)
            _G_not_1315, lastError = self._not(_G_not_1309)
            self.considerError(lastError, 'OctalDigit')
            self._trace('      ', (11026, 11032), self.input.position)
            _G_apply_1316, lastError = self._apply(self.rule_digit, "digit", [])
            self.considerError(lastError, 'OctalDigit')
            return (_G_apply_1316, self.currentError)


        def rule_OctalInteger(self):
            _locals = {'self': self}
            self.locals['OctalInteger'] = _locals
            self._trace("%'\n ", (11048, 11052), self.input.position)
            _G_exactly_1317, lastError = self.exactly('0')
            self.considerError(lastError, 'OctalInteger')
            def _G_consumedby_1318():
                def _G_many1_1319():
                    self._trace('          ', (11054, 11064), self.input.position)
                    _G_apply_1320, lastError = self._apply(self.rule_OctalDigit, "OctalDigit", [])
                    self.considerError(lastError, None)
                    return (_G_apply_1320, self.currentError)
                _G_many1_1321, lastError = self.many(_G_many1_1319, _G_many1_1319())
                self.considerError(lastError, None)
                return (_G_many1_1321, self.currentError)
            _G_consumedby_1322, lastError = self.consumedby(_G_consumedby_1318)
            self.considerError(lastError, 'OctalInteger')
            _locals['ds'] = _G_consumedby_1322
            _G_python_1324, lastError = eval(self._G_expr_1323, self.globals, _locals), None
            self.considerError(lastError, 'OctalInteger')
            return (_G_python_1324, self.currentError)


        def rule_HexDigit(self):
            _locals = {'self': self}
            self.locals['HexDigit'] = _locals
            def _G_or_1325():
                self._trace('      ', (11095, 11101), self.input.position)
                _G_apply_1326, lastError = self._apply(self.rule_digit, "digit", [])
                self.considerError(lastError, None)
                return (_G_apply_1326, self.currentError)
            def _G_or_1327():
                self._trace('  ', (11103, 11105), self.input.position)
                _G_apply_1328, lastError = self._apply(self.rule_A, "A", [])
                self.considerError(lastError, None)
                return (_G_apply_1328, self.currentError)
            def _G_or_1329():
                self._trace('  ', (11107, 11109), self.input.position)
                _G_apply_1330, lastError = self._apply(self.rule_B, "B", [])
                self.considerError(lastError, None)
                return (_G_apply_1330, self.currentError)
            def _G_or_1331():
                self._trace('ou', (11111, 11113), self.input.position)
                _G_apply_1332, lastError = self._apply(self.rule_C, "C", [])
                self.considerError(lastError, None)
                return (_G_apply_1332, self.currentError)
            def _G_or_1333():
                self._trace('eL', (11115, 11117), self.input.position)
                _G_apply_1334, lastError = self._apply(self.rule_D, "D", [])
                self.considerError(lastError, None)
                return (_G_apply_1334, self.currentError)
            def _G_or_1335():
                self._trace('er', (11119, 11121), self.input.position)
                _G_apply_1336, lastError = self._apply(self.rule_E, "E", [])
                self.considerError(lastError, None)
                return (_G_apply_1336, self.currentError)
            def _G_or_1337():
                self._trace('\n ', (11123, 11125), self.input.position)
                _G_apply_1338, lastError = self._apply(self.rule_F, "F", [])
                self.considerError(lastError, None)
                return (_G_apply_1338, self.currentError)
            _G_or_1339, lastError = self._or([_G_or_1325, _G_or_1327, _G_or_1329, _G_or_1331, _G_or_1333, _G_or_1335, _G_or_1337])
            self.considerError(lastError, 'HexDigit')
            return (_G_or_1339, self.currentError)


        def rule_HexInteger(self):
            _locals = {'self': self}
            self.locals['HexInteger'] = _locals
            self._trace('   |', (11139, 11143), self.input.position)
            _G_exactly_1340, lastError = self.exactly('0')
            self.considerError(lastError, 'HexInteger')
            self._trace(' I', (11143, 11145), self.input.position)
            _G_apply_1341, lastError = self._apply(self.rule_X, "X", [])
            self.considerError(lastError, 'HexInteger')
            def _G_consumedby_1342():
                def _G_many1_1343():
                    self._trace('egerLite', (11147, 11155), self.input.position)
                    _G_apply_1344, lastError = self._apply(self.rule_HexDigit, "HexDigit", [])
                    self.considerError(lastError, None)
                    return (_G_apply_1344, self.currentError)
                _G_many1_1345, lastError = self.many(_G_many1_1343, _G_many1_1343())
                self.considerError(lastError, None)
                return (_G_many1_1345, self.currentError)
            _G_consumedby_1346, lastError = self.consumedby(_G_consumedby_1342)
            self.considerError(lastError, 'HexInteger')
            _locals['ds'] = _G_consumedby_1346
            _G_python_1348, lastError = eval(self._G_expr_1347, self.globals, _locals), None
            self.considerError(lastError, 'HexInteger')
            return (_G_python_1348, self.currentError)


        def rule_DecimalInteger(self):
            _locals = {'self': self}
            self.locals['DecimalInteger'] = _locals
            def _G_consumedby_1349():
                def _G_many1_1350():
                    self._trace(' l]\n\n', (11195, 11200), self.input.position)
                    _G_apply_1351, lastError = self._apply(self.rule_digit, "digit", [])
                    self.considerError(lastError, None)
                    return (_G_apply_1351, self.currentError)
                _G_many1_1352, lastError = self.many(_G_many1_1350, _G_many1_1350())
                self.considerError(lastError, None)
                return (_G_many1_1352, self.currentError)
            _G_consumedby_1353, lastError = self.consumedby(_G_consumedby_1349)
            self.considerError(lastError, 'DecimalInteger')
            _locals['ds'] = _G_consumedby_1353
            _G_python_1355, lastError = eval(self._G_expr_1354, self.globals, _locals), None
            self.considerError(lastError, 'DecimalInteger')
            return (_G_python_1355, self.currentError)


        def rule_DoubleLiteral(self):
            _locals = {'self': self}
            self.locals['DoubleLiteral'] = _locals
            def _G_or_1356():
                self._trace('        (\n          ', (11233, 11253), self.input.position)
                _G_apply_1357, lastError = self._apply(self.rule_ExponentDecimalReal, "ExponentDecimalReal", [])
                self.considerError(lastError, None)
                return (_G_apply_1357, self.currentError)
            def _G_or_1358():
                self._trace('                   ', (11269, 11288), self.input.position)
                _G_apply_1359, lastError = self._apply(self.rule_RegularDecimalReal, "RegularDecimalReal", [])
                self.considerError(lastError, None)
                return (_G_apply_1359, self.currentError)
            _G_or_1360, lastError = self._or([_G_or_1356, _G_or_1358])
            self.considerError(lastError, 'DoubleLiteral')
            return (_G_or_1360, self.currentError)


        def rule_ExponentDecimalReal(self):
            _locals = {'self': self}
            self.locals['ExponentDecimalReal'] = _locals
            def _G_consumedby_1361():
                def _G_or_1362():
                    self._trace('WS Expression:v ->', (11314, 11332), self.input.position)
                    _G_apply_1363, lastError = self._apply(self.rule_RegularDecimalReal, "RegularDecimalReal", [])
                    self.considerError(lastError, None)
                    return (_G_apply_1363, self.currentError)
                def _G_or_1364():
                    self._trace('k, v)\n         ', (11334, 11349), self.input.position)
                    _G_apply_1365, lastError = self._apply(self.rule_DecimalInteger, "DecimalInteger", [])
                    self.considerError(lastError, None)
                    return (_G_apply_1365, self.currentError)
                _G_or_1366, lastError = self._or([_G_or_1362, _G_or_1364])
                self.considerError(lastError, None)
                self._trace('  ', (11350, 11352), self.input.position)
                _G_apply_1367, lastError = self._apply(self.rule_E, "E", [])
                self.considerError(lastError, None)
                def _G_optional_1368():
                    def _G_or_1369():
                        self._trace('   ', (11354, 11357), self.input.position)
                        _G_exactly_1370, lastError = self.exactly('+')
                        self.considerError(lastError, None)
                        return (_G_exactly_1370, self.currentError)
                    def _G_or_1371():
                        self._trace(' ):h', (11359, 11363), self.input.position)
                        _G_exactly_1372, lastError = self.exactly('-')
                        self.considerError(lastError, None)
                        return (_G_exactly_1372, self.currentError)
                    _G_or_1373, lastError = self._or([_G_or_1369, _G_or_1371])
                    self.considerError(lastError, None)
                    return (_G_or_1373, self.currentError)
                def _G_optional_1374():
                    return (None, self.input.nullError())
                _G_or_1375, lastError = self._or([_G_optional_1368, _G_optional_1374])
                self.considerError(lastError, None)
                self._trace('d WS\n          ', (11365, 11380), self.input.position)
                _G_apply_1376, lastError = self._apply(self.rule_DecimalInteger, "DecimalInteger", [])
                self.considerError(lastError, None)
                return (_G_apply_1376, self.currentError)
            _G_consumedby_1377, lastError = self.consumedby(_G_consumedby_1361)
            self.considerError(lastError, 'ExponentDecimalReal')
            _locals['ds'] = _G_consumedby_1377
            _G_python_1379, lastError = eval(self._G_expr_1378, self.globals, _locals), None
            self.considerError(lastError, 'ExponentDecimalReal')
            return (_G_python_1379, self.currentError)


        def rule_RegularDecimalReal(self):
            _locals = {'self': self}
            self.locals['RegularDecimalReal'] = _locals
            def _G_or_1380():
                def _G_consumedby_1381():
                    def _G_many1_1382():
                        self._trace(' Prop', (11422, 11427), self.input.position)
                        _G_apply_1383, lastError = self._apply(self.rule_digit, "digit", [])
                        self.considerError(lastError, None)
                        return (_G_apply_1383, self.currentError)
                    _G_many1_1384, lastError = self.many(_G_many1_1382, _G_many1_1382())
                    self.considerError(lastError, None)
                    self._trace('rtyK', (11428, 11432), self.input.position)
                    _G_exactly_1385, lastError = self.exactly('.')
                    self.considerError(lastError, None)
                    def _G_many1_1386():
                        self._trace('eyName', (11432, 11438), self.input.position)
                        _G_apply_1387, lastError = self._apply(self.rule_digit, "digit", [])
                        self.considerError(lastError, None)
                        return (_G_apply_1387, self.currentError)
                    _G_many1_1388, lastError = self.many(_G_many1_1386, _G_many1_1386())
                    self.considerError(lastError, None)
                    return (_G_many1_1388, self.currentError)
                _G_consumedby_1389, lastError = self.consumedby(_G_consumedby_1381)
                self.considerError(lastError, None)
                return (_G_consumedby_1389, self.currentError)
            def _G_or_1390():
                def _G_consumedby_1391():
                    def _G_many1_1392():
                        self._trace("':' W", (11444, 11449), self.input.position)
                        _G_apply_1393, lastError = self._apply(self.rule_digit, "digit", [])
                        self.considerError(lastError, None)
                        return (_G_apply_1393, self.currentError)
                    _G_many1_1394, lastError = self.many(_G_many1_1392, _G_many1_1392())
                    self.considerError(lastError, None)
                    self._trace(' Exp', (11450, 11454), self.input.position)
                    _G_exactly_1395, lastError = self.exactly('.')
                    self.considerError(lastError, None)
                    return (_G_exactly_1395, self.currentError)
                _G_consumedby_1396, lastError = self.consumedby(_G_consumedby_1391)
                self.considerError(lastError, None)
                return (_G_consumedby_1396, self.currentError)
            def _G_or_1397():
                def _G_consumedby_1398():
                    self._trace('on:', (11459, 11462), self.input.position)
                    _G_exactly_1399, lastError = self.exactly('.')
                    self.considerError(lastError, None)
                    def _G_many1_1400():
                        self._trace('v WS -', (11462, 11468), self.input.position)
                        _G_apply_1401, lastError = self._apply(self.rule_digit, "digit", [])
                        self.considerError(lastError, None)
                        return (_G_apply_1401, self.currentError)
                    _G_many1_1402, lastError = self.many(_G_many1_1400, _G_many1_1400())
                    self.considerError(lastError, None)
                    return (_G_many1_1402, self.currentError)
                _G_consumedby_1403, lastError = self.consumedby(_G_consumedby_1398)
                self.considerError(lastError, None)
                return (_G_consumedby_1403, self.currentError)
            _G_or_1404, lastError = self._or([_G_or_1380, _G_or_1390, _G_or_1397])
            self.considerError(lastError, 'RegularDecimalReal')
            _locals['ds'] = _G_or_1404
            _G_python_1405, lastError = eval(self._G_expr_1378, self.globals, _locals), None
            self.considerError(lastError, 'RegularDecimalReal')
            return (_G_python_1405, self.currentError)


        def rule_SymbolicName(self):
            _locals = {'self': self}
            self.locals['SymbolicName'] = _locals
            def _G_or_1406():
                self._trace('l -> [head] + tail\n   ', (11503, 11525), self.input.position)
                _G_apply_1407, lastError = self._apply(self.rule_UnescapedSymbolicName, "UnescapedSymbolicName", [])
                self.considerError(lastError, None)
                return (_G_apply_1407, self.currentError)
            def _G_or_1408():
                self._trace(' -> []):pairs\n      ', (11540, 11560), self.input.position)
                _G_apply_1409, lastError = self._apply(self.rule_EscapedSymbolicName, "EscapedSymbolicName", [])
                self.considerError(lastError, None)
                return (_G_apply_1409, self.currentError)
            _G_or_1410, lastError = self._or([_G_or_1406, _G_or_1408])
            self.considerError(lastError, 'SymbolicName')
            return (_G_or_1410, self.currentError)


        def rule_UnescapedSymbolicName(self):
            _locals = {'self': self}
            self.locals['UnescapedSymbolicName'] = _locals
            def _G_consumedby_1411():
                self._trace(', dict', (11587, 11593), self.input.position)
                _G_apply_1412, lastError = self._apply(self.rule_letter, "letter", [])
                self.considerError(lastError, None)
                def _G_many_1413():
                    def _G_or_1414():
                        self._trace('air', (11595, 11598), self.input.position)
                        _G_exactly_1415, lastError = self.exactly('_')
                        self.considerError(lastError, None)
                        return (_G_exactly_1415, self.currentError)
                    def _G_or_1416():
                        self._trace(']\n\n    Paramet', (11600, 11614), self.input.position)
                        _G_apply_1417, lastError = self._apply(self.rule_letterOrDigit, "letterOrDigit", [])
                        self.considerError(lastError, None)
                        return (_G_apply_1417, self.currentError)
                    _G_or_1418, lastError = self._or([_G_or_1414, _G_or_1416])
                    self.considerError(lastError, None)
                    return (_G_or_1418, self.currentError)
                _G_many_1419, lastError = self.many(_G_many_1413)
                self.considerError(lastError, None)
                return (_G_many_1419, self.currentError)
            _G_consumedby_1420, lastError = self.consumedby(_G_consumedby_1411)
            self.considerError(lastError, 'UnescapedSymbolicName')
            return (_G_consumedby_1420, self.currentError)


        def rule_EscapedSymbolicName(self):
            _locals = {'self': self}
            self.locals['EscapedSymbolicName'] = _locals
            self._trace('ecim', (11640, 11644), self.input.position)
            _G_exactly_1421, lastError = self.exactly('`')
            self.considerError(lastError, 'EscapedSymbolicName')
            def _G_many_1422():
                def _G_or_1423():
                    def _G_not_1424():
                        self._trace('nte', (11647, 11650), self.input.position)
                        _G_exactly_1425, lastError = self.exactly('`')
                        self.considerError(lastError, None)
                        return (_G_exactly_1425, self.currentError)
                    _G_not_1426, lastError = self._not(_G_not_1424)
                    self.considerError(lastError, None)
                    self._trace('ger):p ->', (11650, 11659), self.input.position)
                    _G_apply_1427, lastError = self._apply(self.rule_anything, "anything", [])
                    self.considerError(lastError, None)
                    return (_G_apply_1427, self.currentError)
                def _G_or_1428():
                    self._trace('"Para', (11661, 11666), self.input.position)
                    _G_apply_1429, lastError = self._apply(self.rule_token, "token", ["``"])
                    self.considerError(lastError, None)
                    _G_python_1430, lastError = ('`'), None
                    self.considerError(lastError, None)
                    return (_G_python_1430, self.currentError)
                _G_or_1431, lastError = self._or([_G_or_1423, _G_or_1428])
                self.considerError(lastError, None)
                return (_G_or_1431, self.currentError)
            _G_many_1432, lastError = self.many(_G_many_1422)
            self.considerError(lastError, 'EscapedSymbolicName')
            _locals['cs'] = _G_many_1432
            self._trace('    ', (11678, 11682), self.input.position)
            _G_exactly_1433, lastError = self.exactly('`')
            self.considerError(lastError, 'EscapedSymbolicName')
            _G_python_1434, lastError = eval(self._G_expr_1202, self.globals, _locals), None
            self.considerError(lastError, 'EscapedSymbolicName')
            return (_G_python_1434, self.currentError)


        def rule_WS(self):
            _locals = {'self': self}
            self.locals['WS'] = _locals
            def _G_many_1435():
                self._trace('Atom:a (WS ', (11703, 11714), self.input.position)
                _G_apply_1436, lastError = self._apply(self.rule_whitespace, "whitespace", [])
                self.considerError(lastError, None)
                return (_G_apply_1436, self.currentError)
            _G_many_1437, lastError = self.many(_G_many_1435)
            self.considerError(lastError, 'WS')
            return (_G_many_1437, self.currentError)


        def rule_SP(self):
            _locals = {'self': self}
            self.locals['SP'] = _locals
            def _G_many1_1438():
                self._trace('yLookup)*:o', (11721, 11732), self.input.position)
                _G_apply_1439, lastError = self._apply(self.rule_whitespace, "whitespace", [])
                self.considerError(lastError, None)
                return (_G_apply_1439, self.currentError)
            _G_many1_1440, lastError = self.many(_G_many1_1438, _G_many1_1438())
            self.considerError(lastError, 'SP')
            return (_G_many1_1440, self.currentError)


        def rule_whitespace(self):
            _locals = {'self': self}
            self.locals['whitespace'] = _locals
            def _G_or_1441():
                self._trace('sion', (11747, 11751), self.input.position)
                _G_exactly_1442, lastError = self.exactly(' ')
                self.considerError(lastError, None)
                return (_G_exactly_1442, self.currentError)
            def _G_or_1443():
                self._trace('    P', (11764, 11769), self.input.position)
                _G_exactly_1444, lastError = self.exactly('\t')
                self.considerError(lastError, None)
                return (_G_exactly_1444, self.currentError)
            def _G_or_1445():
                self._trace('e = S', (11782, 11787), self.input.position)
                _G_exactly_1446, lastError = self.exactly('\n')
                self.considerError(lastError, None)
                return (_G_exactly_1446, self.currentError)
            def _G_or_1447():
                self._trace('    Inte', (11800, 11808), self.input.position)
                _G_apply_1448, lastError = self._apply(self.rule_Comment, "Comment", [])
                self.considerError(lastError, None)
                return (_G_apply_1448, self.currentError)
            _G_or_1449, lastError = self._or([_G_or_1441, _G_or_1443, _G_or_1445, _G_or_1447])
            self.considerError(lastError, 'whitespace')
            return (_G_or_1449, self.currentError)


        def rule_Comment(self):
            _locals = {'self': self}
            self.locals['Comment'] = _locals
            def _G_or_1450():
                self._trace('= Hex', (11819, 11824), self.input.position)
                _G_apply_1451, lastError = self._apply(self.rule_token, "token", ["/*"])
                self.considerError(lastError, None)
                def _G_many_1452():
                    def _G_not_1453():
                        self._trace('eger', (11827, 11831), self.input.position)
                        _G_apply_1454, lastError = self._apply(self.rule_token, "token", ["*/"])
                        self.considerError(lastError, None)
                        return (_G_apply_1454, self.currentError)
                    _G_not_1455, lastError = self._not(_G_not_1453)
                    self.considerError(lastError, None)
                    self._trace('\n        ', (11831, 11840), self.input.position)
                    _G_apply_1456, lastError = self._apply(self.rule_anything, "anything", [])
                    self.considerError(lastError, None)
                    return (_G_apply_1456, self.currentError)
                _G_many_1457, lastError = self.many(_G_many_1452)
                self.considerError(lastError, None)
                self._trace('     ', (11842, 11847), self.input.position)
                _G_apply_1458, lastError = self._apply(self.rule_token, "token", ["*/"])
                self.considerError(lastError, None)
                return (_G_apply_1458, self.currentError)
            def _G_or_1459():
                self._trace('lInte', (11857, 11862), self.input.position)
                _G_apply_1460, lastError = self._apply(self.rule_token, "token", ["//"])
                self.considerError(lastError, None)
                def _G_many_1461():
                    def _G_not_1462():
                        def _G_or_1463():
                            self._trace('    ', (11866, 11870), self.input.position)
                            _G_exactly_1464, lastError = self.exactly('\r')
                            self.considerError(lastError, None)
                            return (_G_exactly_1464, self.currentError)
                        def _G_or_1465():
                            self._trace('    ', (11871, 11875), self.input.position)
                            _G_exactly_1466, lastError = self.exactly('\n')
                            self.considerError(lastError, None)
                            return (_G_exactly_1466, self.currentError)
                        _G_or_1467, lastError = self._or([_G_or_1463, _G_or_1465])
                        self.considerError(lastError, None)
                        return (_G_or_1467, self.currentError)
                    _G_not_1468, lastError = self._not(_G_not_1462)
                    self.considerError(lastError, None)
                    self._trace('         ', (11876, 11885), self.input.position)
                    _G_apply_1469, lastError = self._apply(self.rule_anything, "anything", [])
                    self.considerError(lastError, None)
                    return (_G_apply_1469, self.currentError)
                _G_many_1470, lastError = self.many(_G_many_1461)
                self.considerError(lastError, None)
                def _G_optional_1471():
                    self._trace('Decim', (11887, 11892), self.input.position)
                    _G_exactly_1472, lastError = self.exactly('\r')
                    self.considerError(lastError, None)
                    return (_G_exactly_1472, self.currentError)
                def _G_optional_1473():
                    return (None, self.input.nullError())
                _G_or_1474, lastError = self._or([_G_optional_1471, _G_optional_1473])
                self.considerError(lastError, None)
                def _G_or_1475():
                    self._trace('nteg', (11895, 11899), self.input.position)
                    _G_exactly_1476, lastError = self.exactly('\n')
                    self.considerError(lastError, None)
                    return (_G_exactly_1476, self.currentError)
                def _G_or_1477():
                    self._trace('r\n\n', (11900, 11903), self.input.position)
                    _G_apply_1478, lastError = self._apply(self.rule_end, "end", [])
                    self.considerError(lastError, None)
                    return (_G_apply_1478, self.currentError)
                _G_or_1479, lastError = self._or([_G_or_1475, _G_or_1477])
                self.considerError(lastError, None)
                return (_G_or_1479, self.currentError)
            _G_or_1480, lastError = self._or([_G_or_1450, _G_or_1459])
            self.considerError(lastError, 'Comment')
            return (_G_or_1480, self.currentError)


        def rule_LeftArrowHead(self):
            _locals = {'self': self}
            self.locals['LeftArrowHead'] = _locals
            self._trace("('8'", (11921, 11925), self.input.position)
            _G_exactly_1481, lastError = self.exactly('<')
            self.considerError(lastError, 'LeftArrowHead')
            return (_G_exactly_1481, self.currentError)


        def rule_RightArrowHead(self):
            _locals = {'self': self}
            self.locals['RightArrowHead'] = _locals
            self._trace('ctal', (11943, 11947), self.input.position)
            _G_exactly_1482, lastError = self.exactly('>')
            self.considerError(lastError, 'RightArrowHead')
            return (_G_exactly_1482, self.currentError)


        def rule_Dash(self):
            _locals = {'self': self}
            self.locals['Dash'] = _locals
            self._trace("= '0", (11955, 11959), self.input.position)
            _G_exactly_1483, lastError = self.exactly('-')
            self.considerError(lastError, 'Dash')
            return (_G_exactly_1483, self.currentError)


        def rule_A(self):
            _locals = {'self': self}
            self.locals['A'] = _locals
            def _G_or_1484():
                self._trace('talD', (11964, 11968), self.input.position)
                _G_exactly_1485, lastError = self.exactly('A')
                self.considerError(lastError, None)
                return (_G_exactly_1485, self.currentError)
            def _G_or_1486():
                self._trace('it+>', (11970, 11974), self.input.position)
                _G_exactly_1487, lastError = self.exactly('a')
                self.considerError(lastError, None)
                return (_G_exactly_1487, self.currentError)
            _G_or_1488, lastError = self._or([_G_or_1484, _G_or_1486])
            self.considerError(lastError, 'A')
            return (_G_or_1488, self.currentError)


        def rule_B(self):
            _locals = {'self': self}
            self.locals['B'] = _locals
            def _G_or_1489():
                self._trace('> in', (11979, 11983), self.input.position)
                _G_exactly_1490, lastError = self.exactly('B')
                self.considerError(lastError, None)
                return (_G_exactly_1490, self.currentError)
            def _G_or_1491():
                self._trace('ds, ', (11985, 11989), self.input.position)
                _G_exactly_1492, lastError = self.exactly('b')
                self.considerError(lastError, None)
                return (_G_exactly_1492, self.currentError)
            _G_or_1493, lastError = self._or([_G_or_1489, _G_or_1491])
            self.considerError(lastError, 'B')
            return (_G_or_1493, self.currentError)


        def rule_C(self):
            _locals = {'self': self}
            self.locals['C'] = _locals
            def _G_or_1494():
                self._trace('   H', (11994, 11998), self.input.position)
                _G_exactly_1495, lastError = self.exactly('C')
                self.considerError(lastError, None)
                return (_G_exactly_1495, self.currentError)
            def _G_or_1496():
                self._trace('Digi', (12000, 12004), self.input.position)
                _G_exactly_1497, lastError = self.exactly('c')
                self.considerError(lastError, None)
                return (_G_exactly_1497, self.currentError)
            _G_or_1498, lastError = self._or([_G_or_1494, _G_or_1496])
            self.considerError(lastError, 'C')
            return (_G_or_1498, self.currentError)


        def rule_D(self):
            _locals = {'self': self}
            self.locals['D'] = _locals
            def _G_or_1499():
                self._trace('igit', (12009, 12013), self.input.position)
                _G_exactly_1500, lastError = self.exactly('D')
                self.considerError(lastError, None)
                return (_G_exactly_1500, self.currentError)
            def _G_or_1501():
                self._trace(' A |', (12015, 12019), self.input.position)
                _G_exactly_1502, lastError = self.exactly('d')
                self.considerError(lastError, None)
                return (_G_exactly_1502, self.currentError)
            _G_or_1503, lastError = self._or([_G_or_1499, _G_or_1501])
            self.considerError(lastError, 'D')
            return (_G_or_1503, self.currentError)


        def rule_E(self):
            _locals = {'self': self}
            self.locals['E'] = _locals
            def _G_or_1504():
                self._trace('C | ', (12024, 12028), self.input.position)
                _G_exactly_1505, lastError = self.exactly('E')
                self.considerError(lastError, None)
                return (_G_exactly_1505, self.currentError)
            def _G_or_1506():
                self._trace('| E ', (12030, 12034), self.input.position)
                _G_exactly_1507, lastError = self.exactly('e')
                self.considerError(lastError, None)
                return (_G_exactly_1507, self.currentError)
            _G_or_1508, lastError = self._or([_G_or_1504, _G_or_1506])
            self.considerError(lastError, 'E')
            return (_G_or_1508, self.currentError)


        def rule_F(self):
            _locals = {'self': self}
            self.locals['F'] = _locals
            def _G_or_1509():
                self._trace('    ', (12039, 12043), self.input.position)
                _G_exactly_1510, lastError = self.exactly('F')
                self.considerError(lastError, None)
                return (_G_exactly_1510, self.currentError)
            def _G_or_1511():
                self._trace('xInt', (12045, 12049), self.input.position)
                _G_exactly_1512, lastError = self.exactly('f')
                self.considerError(lastError, None)
                return (_G_exactly_1512, self.currentError)
            _G_or_1513, lastError = self._or([_G_or_1509, _G_or_1511])
            self.considerError(lastError, 'F')
            return (_G_or_1513, self.currentError)


        def rule_G(self):
            _locals = {'self': self}
            self.locals['G'] = _locals
            def _G_or_1514():
                self._trace("= '0", (12054, 12058), self.input.position)
                _G_exactly_1515, lastError = self.exactly('G')
                self.considerError(lastError, None)
                return (_G_exactly_1515, self.currentError)
            def _G_or_1516():
                self._trace('X <H', (12060, 12064), self.input.position)
                _G_exactly_1517, lastError = self.exactly('g')
                self.considerError(lastError, None)
                return (_G_exactly_1517, self.currentError)
            _G_or_1518, lastError = self._or([_G_or_1514, _G_or_1516])
            self.considerError(lastError, 'G')
            return (_G_or_1518, self.currentError)


        def rule_H(self):
            _locals = {'self': self}
            self.locals['H'] = _locals
            def _G_or_1519():
                self._trace('it+>', (12069, 12073), self.input.position)
                _G_exactly_1520, lastError = self.exactly('H')
                self.considerError(lastError, None)
                return (_G_exactly_1520, self.currentError)
            def _G_or_1521():
                self._trace('s ->', (12075, 12079), self.input.position)
                _G_exactly_1522, lastError = self.exactly('h')
                self.considerError(lastError, None)
                return (_G_exactly_1522, self.currentError)
            _G_or_1523, lastError = self._or([_G_or_1519, _G_or_1521])
            self.considerError(lastError, 'H')
            return (_G_or_1523, self.currentError)


        def rule_I(self):
            _locals = {'self': self}
            self.locals['I'] = _locals
            def _G_or_1524():
                self._trace('ds, ', (12084, 12088), self.input.position)
                _G_exactly_1525, lastError = self.exactly('I')
                self.considerError(lastError, None)
                return (_G_exactly_1525, self.currentError)
            def _G_or_1526():
                self._trace(')\n\n ', (12090, 12094), self.input.position)
                _G_exactly_1527, lastError = self.exactly('i')
                self.considerError(lastError, None)
                return (_G_exactly_1527, self.currentError)
            _G_or_1528, lastError = self._or([_G_or_1524, _G_or_1526])
            self.considerError(lastError, 'I')
            return (_G_or_1528, self.currentError)


        def rule_K(self):
            _locals = {'self': self}
            self.locals['K'] = _locals
            def _G_or_1529():
                self._trace('cima', (12099, 12103), self.input.position)
                _G_exactly_1530, lastError = self.exactly('K')
                self.considerError(lastError, None)
                return (_G_exactly_1530, self.currentError)
            def _G_or_1531():
                self._trace('nteg', (12105, 12109), self.input.position)
                _G_exactly_1532, lastError = self.exactly('k')
                self.considerError(lastError, None)
                return (_G_exactly_1532, self.currentError)
            _G_or_1533, lastError = self._or([_G_or_1529, _G_or_1531])
            self.considerError(lastError, 'K')
            return (_G_or_1533, self.currentError)


        def rule_L(self):
            _locals = {'self': self}
            self.locals['L'] = _locals
            def _G_or_1534():
                self._trace('<dig', (12114, 12118), self.input.position)
                _G_exactly_1535, lastError = self.exactly('L')
                self.considerError(lastError, None)
                return (_G_exactly_1535, self.currentError)
            def _G_or_1536():
                self._trace('+>:d', (12120, 12124), self.input.position)
                _G_exactly_1537, lastError = self.exactly('l')
                self.considerError(lastError, None)
                return (_G_exactly_1537, self.currentError)
            _G_or_1538, lastError = self._or([_G_or_1534, _G_or_1536])
            self.considerError(lastError, 'L')
            return (_G_or_1538, self.currentError)


        def rule_M(self):
            _locals = {'self': self}
            self.locals['M'] = _locals
            def _G_or_1539():
                self._trace('int(', (12129, 12133), self.input.position)
                _G_exactly_1540, lastError = self.exactly('M')
                self.considerError(lastError, None)
                return (_G_exactly_1540, self.currentError)
            def _G_or_1541():
                self._trace(')\n\n ', (12135, 12139), self.input.position)
                _G_exactly_1542, lastError = self.exactly('m')
                self.considerError(lastError, None)
                return (_G_exactly_1542, self.currentError)
            _G_or_1543, lastError = self._or([_G_or_1539, _G_or_1541])
            self.considerError(lastError, 'M')
            return (_G_or_1543, self.currentError)


        def rule_N(self):
            _locals = {'self': self}
            self.locals['N'] = _locals
            def _G_or_1544():
                self._trace('uble', (12144, 12148), self.input.position)
                _G_exactly_1545, lastError = self.exactly('N')
                self.considerError(lastError, None)
                return (_G_exactly_1545, self.currentError)
            def _G_or_1546():
                self._trace('tera', (12150, 12154), self.input.position)
                _G_exactly_1547, lastError = self.exactly('n')
                self.considerError(lastError, None)
                return (_G_exactly_1547, self.currentError)
            _G_or_1548, lastError = self._or([_G_or_1544, _G_or_1546])
            self.considerError(lastError, 'N')
            return (_G_or_1548, self.currentError)


        def rule_O(self):
            _locals = {'self': self}
            self.locals['O'] = _locals
            def _G_or_1549():
                self._trace('xpon', (12159, 12163), self.input.position)
                _G_exactly_1550, lastError = self.exactly('O')
                self.considerError(lastError, None)
                return (_G_exactly_1550, self.currentError)
            def _G_or_1551():
                self._trace('tDec', (12165, 12169), self.input.position)
                _G_exactly_1552, lastError = self.exactly('o')
                self.considerError(lastError, None)
                return (_G_exactly_1552, self.currentError)
            _G_or_1553, lastError = self._or([_G_or_1549, _G_or_1551])
            self.considerError(lastError, 'O')
            return (_G_or_1553, self.currentError)


        def rule_P(self):
            _locals = {'self': self}
            self.locals['P'] = _locals
            def _G_or_1554():
                self._trace('eal\n', (12174, 12178), self.input.position)
                _G_exactly_1555, lastError = self.exactly('P')
                self.considerError(lastError, None)
                return (_G_exactly_1555, self.currentError)
            def _G_or_1556():
                self._trace('    ', (12180, 12184), self.input.position)
                _G_exactly_1557, lastError = self.exactly('p')
                self.considerError(lastError, None)
                return (_G_exactly_1557, self.currentError)
            _G_or_1558, lastError = self._or([_G_or_1554, _G_or_1556])
            self.considerError(lastError, 'P')
            return (_G_or_1558, self.currentError)


        def rule_R(self):
            _locals = {'self': self}
            self.locals['R'] = _locals
            def _G_or_1559():
                self._trace('    ', (12189, 12193), self.input.position)
                _G_exactly_1560, lastError = self.exactly('R')
                self.considerError(lastError, None)
                return (_G_exactly_1560, self.currentError)
            def _G_or_1561():
                self._trace(' | R', (12195, 12199), self.input.position)
                _G_exactly_1562, lastError = self.exactly('r')
                self.considerError(lastError, None)
                return (_G_exactly_1562, self.currentError)
            _G_or_1563, lastError = self._or([_G_or_1559, _G_or_1561])
            self.considerError(lastError, 'R')
            return (_G_or_1563, self.currentError)


        def rule_S(self):
            _locals = {'self': self}
            self.locals['S'] = _locals
            def _G_or_1564():
                self._trace('rDec', (12204, 12208), self.input.position)
                _G_exactly_1565, lastError = self.exactly('S')
                self.considerError(lastError, None)
                return (_G_exactly_1565, self.currentError)
            def _G_or_1566():
                self._trace('alRe', (12210, 12214), self.input.position)
                _G_exactly_1567, lastError = self.exactly('s')
                self.considerError(lastError, None)
                return (_G_exactly_1567, self.currentError)
            _G_or_1568, lastError = self._or([_G_or_1564, _G_or_1566])
            self.considerError(lastError, 'S')
            return (_G_or_1568, self.currentError)


        def rule_T(self):
            _locals = {'self': self}
            self.locals['T'] = _locals
            def _G_or_1569():
                self._trace('   E', (12219, 12223), self.input.position)
                _G_exactly_1570, lastError = self.exactly('T')
                self.considerError(lastError, None)
                return (_G_exactly_1570, self.currentError)
            def _G_or_1571():
                self._trace('onen', (12225, 12229), self.input.position)
                _G_exactly_1572, lastError = self.exactly('t')
                self.considerError(lastError, None)
                return (_G_exactly_1572, self.currentError)
            _G_or_1573, lastError = self._or([_G_or_1569, _G_or_1571])
            self.considerError(lastError, 'T')
            return (_G_or_1573, self.currentError)


        def rule_U(self):
            _locals = {'self': self}
            self.locals['U'] = _locals
            def _G_or_1574():
                self._trace('malR', (12234, 12238), self.input.position)
                _G_exactly_1575, lastError = self.exactly('U')
                self.considerError(lastError, None)
                return (_G_exactly_1575, self.currentError)
            def _G_or_1576():
                self._trace('l = ', (12240, 12244), self.input.position)
                _G_exactly_1577, lastError = self.exactly('u')
                self.considerError(lastError, None)
                return (_G_exactly_1577, self.currentError)
            _G_or_1578, lastError = self._or([_G_or_1574, _G_or_1576])
            self.considerError(lastError, 'U')
            return (_G_or_1578, self.currentError)


        def rule_V(self):
            _locals = {'self': self}
            self.locals['V'] = _locals
            def _G_or_1579():
                self._trace('ular', (12249, 12253), self.input.position)
                _G_exactly_1580, lastError = self.exactly('V')
                self.considerError(lastError, None)
                return (_G_exactly_1580, self.currentError)
            def _G_or_1581():
                self._trace('cima', (12255, 12259), self.input.position)
                _G_exactly_1582, lastError = self.exactly('v')
                self.considerError(lastError, None)
                return (_G_exactly_1582, self.currentError)
            _G_or_1583, lastError = self._or([_G_or_1579, _G_or_1581])
            self.considerError(lastError, 'V')
            return (_G_or_1583, self.currentError)


        def rule_W(self):
            _locals = {'self': self}
            self.locals['W'] = _locals
            def _G_or_1584():
                self._trace(' | D', (12264, 12268), self.input.position)
                _G_exactly_1585, lastError = self.exactly('W')
                self.considerError(lastError, None)
                return (_G_exactly_1585, self.currentError)
            def _G_or_1586():
                self._trace('imal', (12270, 12274), self.input.position)
                _G_exactly_1587, lastError = self.exactly('w')
                self.considerError(lastError, None)
                return (_G_exactly_1587, self.currentError)
            _G_or_1588, lastError = self._or([_G_or_1584, _G_or_1586])
            self.considerError(lastError, 'W')
            return (_G_or_1588, self.currentError)


        def rule_X(self):
            _locals = {'self': self}
            self.locals['X'] = _locals
            def _G_or_1589():
                self._trace('er) ', (12279, 12283), self.input.position)
                _G_exactly_1590, lastError = self.exactly('X')
                self.considerError(lastError, None)
                return (_G_exactly_1590, self.currentError)
            def _G_or_1591():
                self._trace("('+'", (12285, 12289), self.input.position)
                _G_exactly_1592, lastError = self.exactly('x')
                self.considerError(lastError, None)
                return (_G_exactly_1592, self.currentError)
            _G_or_1593, lastError = self._or([_G_or_1589, _G_or_1591])
            self.considerError(lastError, 'X')
            return (_G_or_1593, self.currentError)


        def rule_Y(self):
            _locals = {'self': self}
            self.locals['Y'] = _locals
            def _G_or_1594():
                self._trace("')? ", (12294, 12298), self.input.position)
                _G_exactly_1595, lastError = self.exactly('Y')
                self.considerError(lastError, None)
                return (_G_exactly_1595, self.currentError)
            def _G_or_1596():
                self._trace('cima', (12300, 12304), self.input.position)
                _G_exactly_1597, lastError = self.exactly('y')
                self.considerError(lastError, None)
                return (_G_exactly_1597, self.currentError)
            _G_or_1598, lastError = self._or([_G_or_1594, _G_or_1596])
            self.considerError(lastError, 'Y')
            return (_G_or_1598, self.currentError)


        def rule_Z(self):
            _locals = {'self': self}
            self.locals['Z'] = _locals
            def _G_or_1599():
                self._trace('ger>', (12309, 12313), self.input.position)
                _G_exactly_1600, lastError = self.exactly('Z')
                self.considerError(lastError, None)
                return (_G_exactly_1600, self.currentError)
            def _G_or_1601():
                self._trace('s ->', (12315, 12319), self.input.position)
                _G_exactly_1602, lastError = self.exactly('z')
                self.considerError(lastError, None)
                return (_G_exactly_1602, self.currentError)
            _G_or_1603, lastError = self._or([_G_or_1599, _G_or_1601])
            self.considerError(lastError, 'Z')
            return (_G_or_1603, self.currentError)


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
        _G_expr_342 = compile('["Order", [head] + tail]', '<string>', 'eval')
        _G_expr_350 = compile('["Skip", ex]', '<string>', 'eval')
        _G_expr_359 = compile('["Limit", ex]', '<string>', 'eval')
        _G_expr_382 = compile('["sort", ex, "desc"]', '<string>', 'eval')
        _G_expr_406 = compile('["sort", ex, "asc"]', '<string>', 'eval')
        _G_expr_416 = compile('["Where", ex]', '<string>', 'eval')
        _G_expr_424 = compile('[head] + tail', '<string>', 'eval')
        _G_expr_432 = compile('["PatternPart", v, ap]', '<string>', 'eval')
        _G_expr_439 = compile('["GraphPatternPart", v, ap]', '<string>', 'eval')
        _G_expr_443 = compile('["PatternPart", None, ap]', '<string>', 'eval')
        _G_expr_453 = compile('["PatternElement", np, pec]', '<string>', 'eval')
        _G_expr_459 = compile('pe', '<string>', 'eval')
        _G_expr_473 = compile('nl', '<string>', 'eval')
        _G_expr_480 = compile('p', '<string>', 'eval')
        _G_expr_485 = compile('["NodePattern", s, nl, p]', '<string>', 'eval')
        _G_expr_490 = compile('["PatternElementChain", rp, np]', '<string>', 'eval')
        _G_expr_510 = compile('["RelationshipsPattern", la, rd, ra]', '<string>', 'eval')
        _G_expr_536 = compile('["RelationshipDetail", v, q, rt, rl, p]', '<string>', 'eval')
        _G_expr_555 = compile('["RelationshipTypes", head] + tail', '<string>', 'eval')
        _G_expr_565 = compile('["NodeLabel", n]', '<string>', 'eval')
        _G_expr_580 = compile('slice(start, stop)', '<string>', 'eval')
        _G_expr_592 = compile('["or", ex1, ex2]', '<string>', 'eval')
        _G_expr_605 = compile('["xor", ex1, ex2]', '<string>', 'eval')
        _G_expr_618 = compile('["and", ex1, ex2]', '<string>', 'eval')
        _G_expr_629 = compile('["not", ex]', '<string>', 'eval')
        _G_expr_640 = compile('["eq",  ex1, ex2]', '<string>', 'eval')
        _G_expr_648 = compile('["neq", ex1, ex2]', '<string>', 'eval')
        _G_expr_663 = compile('["lt",  ex1, ex2]', '<string>', 'eval')
        _G_expr_671 = compile('["gt",  ex1, ex2]', '<string>', 'eval')
        _G_expr_679 = compile('["lte", ex1, ex2]', '<string>', 'eval')
        _G_expr_687 = compile('["gte", ex1, ex2]', '<string>', 'eval')
        _G_expr_698 = compile('["add", ex1, ex2]', '<string>', 'eval')
        _G_expr_706 = compile('["sub", ex1, ex2]', '<string>', 'eval')
        _G_expr_717 = compile('["multi", ex1, ex2]', '<string>', 'eval')
        _G_expr_725 = compile('["div",   ex1, ex2]', '<string>', 'eval')
        _G_expr_733 = compile('["mod",   ex1, ex2]', '<string>', 'eval')
        _G_expr_744 = compile('["hat", ex1, ex2]', '<string>', 'eval')
        _G_expr_757 = compile('["minus", ex]', '<string>', 'eval')
        _G_expr_770 = compile('["PropertyLookup", prop_name]', '<string>', 'eval')
        _G_expr_785 = compile('["slice", start, end]', '<string>', 'eval')
        _G_expr_837 = compile('[operator, ex2]', '<string>', 'eval')
        _G_expr_865 = compile('["Expression3", ex1, c]', '<string>', 'eval')
        _G_expr_879 = compile('["Expression2", a, c]', '<string>', 'eval')
        _G_expr_936 = compile('item', '<string>', 'eval')
        _G_expr_944 = compile('["List", ex]', '<string>', 'eval')
        _G_expr_959 = compile('["Filter", fex]', '<string>', 'eval')
        _G_expr_981 = compile('["Extract", fex, ex]', '<string>', 'eval')
        _G_expr_993 = compile('["All", fex]', '<string>', 'eval')
        _G_expr_1005 = compile('["Any", fex]', '<string>', 'eval')
        _G_expr_1018 = compile('["None", fex]', '<string>', 'eval')
        _G_expr_1033 = compile('["Single", fex]', '<string>', 'eval')
        _G_expr_1051 = compile('ex', '<string>', 'eval')
        _G_expr_1059 = compile('["RelationshipsPattern", np, pec]', '<string>', 'eval')
        _G_expr_1070 = compile('["GraphRelationshipsPattern", v, np, pec]', '<string>', 'eval')
        _G_expr_1078 = compile('["FilterExpression", i, w]', '<string>', 'eval')
        _G_expr_1086 = compile('["IdInColl", v, ex]', '<string>', 'eval')
        _G_expr_1118 = compile('["call", func, distinct, args]', '<string>', 'eval')
        _G_expr_1130 = compile('["ListComprehension", fex, ex]', '<string>', 'eval')
        _G_expr_1136 = compile('["PropertyLookup", n]', '<string>', 'eval')
        _G_expr_1165 = compile('["Case", ex, cas, el]', '<string>', 'eval')
        _G_expr_1180 = compile('[ex1, ex2]', '<string>', 'eval')
        _G_expr_1183 = compile('["Variable", s]', '<string>', 'eval')
        _G_expr_1202 = compile('"".join(cs)', '<string>', 'eval')
        _G_expr_1223 = compile('["Literal", l]', '<string>', 'eval')
        _G_expr_1265 = compile('(k, v)', '<string>', 'eval')
        _G_expr_1284 = compile('["Literal", dict(pairs)]', '<string>', 'eval')
        _G_expr_1292 = compile('["Parameter", p]', '<string>', 'eval')
        _G_expr_1299 = compile('["Expression", a, opts]', '<string>', 'eval')
        _G_expr_1323 = compile('int(ds, 8)', '<string>', 'eval')
        _G_expr_1347 = compile('int(ds, 16)', '<string>', 'eval')
        _G_expr_1354 = compile('int(ds)', '<string>', 'eval')
        _G_expr_1378 = compile('float(ds)', '<string>', 'eval')
    if Grammar.globals is not None:
        Grammar.globals = Grammar.globals.copy()
        Grammar.globals.update(ruleGlobals)
    else:
        Grammar.globals = ruleGlobals
    return Grammar