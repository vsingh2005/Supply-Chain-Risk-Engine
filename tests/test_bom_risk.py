from supply_chain_risk.bom_risk import BOMRiskAnalyzer

def test_bom_single_source_detection():
    tree = {
        "name": "Vehicle_ECU",
        "suppliers": ["Supplier_A", "Supplier_B"],
        "sub_components": [
            {
                "name": "Microcontroller",
                "suppliers": ["Solo_Semi_Co"],
                "lead_time_weeks": 26,
                "sub_components": []
            }
        ]
    }
    analyzer = BOMRiskAnalyzer(tree)
    single_sources = analyzer.find_single_source_components()
    assert len(single_sources) == 1
    assert single_sources[0]["component"] == "Microcontroller"
