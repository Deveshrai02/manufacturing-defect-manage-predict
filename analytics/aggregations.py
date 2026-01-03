from collections import defaultdict

class DefectAnalytics:
        def defects_by_type(self, defects):
            result = defaultdict(int)
            for defect in defects:
                result[defect.defect_type] += 1
            return dict(result)

        def cost_by_position(self, defects):
            result = defaultdict(float)
            for defect in defects:
                result[defect.defect_location] += defect.repair_cost
            return dict(result)
                
