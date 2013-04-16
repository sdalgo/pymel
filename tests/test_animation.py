import sys
import unittest
import traceback

import maya.cmds as cmds

import pymel.core as pm
import pymel.util as util
import pymel.util.testing as testing

class TestConstraintVectorQuery(testing.TestCaseExtended):
    def setUp(self):
        cmds.file(new=1, f=1)

    def _doTestForConstraintType(self, constraintType):
        cmd = getattr(pm, constraintType)

        if constraintType == 'tangentConstraint':
            target = cmds.circle()[0]
        else:
            target = cmds.polyCube()[0]
        constrained = cmds.polyCube()[0]

        constr = cmd(target, constrained)
        print constr

        self.assertVectorsEqual(cmd(constr, q=1, worldUpVector=1), [0,1,0])
        self.assertVectorsEqual(constr.getWorldUpVector(), [0,1,0])

        self.assertVectorsEqual(cmd(constr, q=1, upVector=1), [0,1,0])
        self.assertVectorsEqual(constr.getUpVector(), [0,1,0])

        self.assertVectorsEqual(cmd(constr, q=1, aimVector=1), [1,0,0])
        self.assertVectorsEqual(constr.getAimVector(), [1,0,0])

    def test_aimConstraint(self):
        self._doTestForConstraintType('aimConstraint')

    def test_normalConstraint(self):
        self._doTestForConstraintType('normalConstraint')

    def test_tangentConstraint(self):
        self._doTestForConstraintType('tangentConstraint')

class TestTimeRange(testing.TestCaseExtended):
    def setUp(self):
        cmds.file(new=1, f=1)
        self.cube = cmds.polyCube()[0]
        for i in xrange(1,21,2):
            cmds.currentTime(i)
            pm.setAttr(self.cube + '.tx', i)
            pm.setKeyframe(self.cube + '.tx')

    def tearDown(self):
        cmds.delete(self.cube)

    @classmethod
    def addTest(cls, func, flag, val, expected):
        # define the test
        def test(self):
            kwargs = {'query':1, 'attribute':'tx', 'keyframeCount':1, flag:val}
            try:
                result = pm.keyframe(self.cube, **kwargs)
            except Exception:
                trace = traceback.format_exc()
                self.fail('Error executing keyframe for %s=%r:\n%s' % (flag, val, trace))
            self.assertEqual(result, expected,
                             "Wrong value for %s=%r - expected %r, got %r" % (flag, val, expected, result))

        # name the test...
        if isinstance(val, basestring):
            valPieces = val.split(':')
        elif isinstance(val, slice):
            valPieces = (val.start, val.stop)
        elif isinstance(val, (list, tuple)):
            valPieces = val
        else:
            valPieces = [val]
        valPieces = ["BLANK" if x == "" else x for x in valPieces]
        if len(valPieces) == 1:
            valName = '%s' % valPieces[0]
        else:
            valName = '%s_%s' % tuple(valPieces)
        valName = '%s_%s' % (type(val).__name__, valName)
        testName = 'test_%s_%s_%s' % (func.__name__, flag, valName)
        test.__name__ = testName

        # add the test to the class
        setattr(cls, testName, test)

    @classmethod
    def addKeyframeTimeTests(cls):
        for val, expected in [
                              ((4,),         0),
                              ((9,),         1),
                              ((None,),     10),
                              ((4,4),        0),
                              ((4,9),        3),
                              ((4,None),     8),
                              ((9,9),        1),
                              ((9,None),     6),
                              ((None,4),     2),
                              ((None,9),     5),
                              ((None,None), 10),

                              ([4,],         0),
                              ([9,],         1),
                              ([None,],     10),
                              ([4,4],        0),
                              ([4,9],        3),
                              ([4,None],     8),
                              ([9,9],        1),
                              ([9,None],     6),
                              ([None,4],     2),
                              ([None,9],     5),
                              ([None,None], 10),


                              ('4:4',        0),
                              ('4:9',        3),
                              ('4:',         8),
                              ('9:9',        1),
                              ('9:',         6),
                              (':4',         2),
                              (':9',         5),
                              (':',         10),

                              (slice(4),          2),
                              (slice(9),          5),
                              (slice(None),      10),
                              (slice(4,4),        0),
                              (slice(4,9),        3),
                              (slice(4,None),     8),
                              (slice(9,9),        1),
                              (slice(9,None),     6),
                              (slice(None,4),     2),
                              (slice(None,9),     5),
                              (slice(None,None), 10),

                              (4,            0),
                              (9,            1),
                             ]:
            cls.addTest(pm.keyframe, 'time', val, expected)
            cls.addTest(pm.keyframe, 't', val, expected)

    @classmethod
    def addKeyframeIndexTests(cls):
        for val, expected in [
                              ((2,),         1),
                              ((8,),         1),
                              ((10,),        0),
                              ((None,),     10),
                              ((10,10),      0),
                              ((2,2),        1),
                              ((2,8),        7),
                              ((2,None),     8),
                              ((8,8),        1),
                              ((8,None),     2),
                              ((None,2),     3),
                              ((None,8),     9),
                              ((None,None), 10),

                              ([2,],         1),
                              ([8,],         1),
                              ([None,],     10),
                              ([10,10],      0),
                              ([2,2],        1),
                              ([2,8],        7),
                              ([2,None],     8),
                              ([8,8],        1),
                              ([8,None],     2),
                              ([None,2],     3),
                              ([None,8],     9),
                              ([None,None], 10),


                              ('10:10',      0),
                              ('2:2',        1),
                              ('2:8',        7),
                              ('2:',         8),
                              ('8:8',        1),
                              ('8:',         2),
                              (':2',         3),
                              (':8',         9),
                              (':',         10),

                              (slice(2),          3),
                              (slice(8),          9),
                              (slice(None),      10),
                              (slice(2,2),        1),
                              (slice(2,8),        7),
                              (slice(2,None),     8),
                              (slice(8,8),        1),
                              (slice(8,None),     2),
                              (slice(None,2),     3),
                              (slice(None,8),     9),
                              (slice(None,None), 10),

                              (4,            1),
                              (9,            1),
                             ]:
            cls.addTest(pm.keyframe, 'index', val, expected)

TestTimeRange.addKeyframeTimeTests()
TestTimeRange.addKeyframeIndexTests()
