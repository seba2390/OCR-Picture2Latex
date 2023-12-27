from typing import List


class ArxivCategories:
    __physics_categories__ = {'Astrophysics': 'astro-ph',
                              'Condensed Matter': 'cond-mat',
                              'General Relativity and Quantum Cosmology': 'qr-qc',
                              'High Energy Physics - Experiment': 'hep-ex',
                              'High Energy Physics - Lattice': 'hep-lat',
                              'High Energy Physics - Phenomenology': 'hep-ph',
                              'High Energy Physics - Theory': 'hep-th',
                              'Mathematical Physics': 'math-ph',
                              'Nonlinear Sciences': 'nlin',
                              'Nuclear Experiment': 'nucl-ex',
                              'Nuclear Theory': 'nucl-th',
                              'Physics': 'physics',
                              'Quantum Physics': 'quant-ph'
                              }

    __mathematics_categories__ = {'Mathematics': 'math'}

    __computer_science_categories__ = {'Computing Research Repository': 'CoRR'}

    __quantitative_biology_categories__ = {'Quantitative Biology': 'q-bio'}

    __quantitative_finance_categories__ = {'Quantitative Finance': 'q-fin'}

    __statistics_categories__ = {'Statistics': 'stat'}

    def __init__(self):
        self.main_categories = {**self.__physics_categories__,
                                **self.__mathematics_categories__,
                                **self.__computer_science_categories__,
                                **self.__quantitative_biology_categories__,
                                **self.__quantitative_finance_categories__,
                                **self.__statistics_categories__}

    def available_category_names(self) -> List[str]:
        return list(self.main_categories.keys())

    def available_category_tags(self) -> List[str]:
        return list(self.main_categories.values())

    def get_tag(self, category_name: str) -> str:
        return self.main_categories[category_name]
