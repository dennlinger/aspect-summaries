import unittest

import spacy
from rouge_score.rouge_scorer import _create_ngrams

from summaries.utils import find_closest_reference_matches, max_rouge_2_match, RelevantSentence


class TestDensityPlot(unittest.TestCase):
    def setUp(self):
        self.processor = spacy.load("de_core_news_sm", disable=("ner",))

    def test_find_closest_reference_match(self):

        extracted_doc = self.processor("Das ist ein Test.")
        reference_doc = self.processor("Ein längerer Inhalt. Er besteht aus mehreren Tests. Das ist ein Test.")

        self.assertEqual([2/3], find_closest_reference_matches(extracted_doc, reference_doc))

    def test_max_rouge_2_match(self):

        extracted_sentence = list(self.processor("Er besteht aus mehreren merkwürdigen Tests").sents)[0]

        reference_doc = self.processor("Ein längerer Inhalt. Er besteht aus mehreren Tests. Das ist ein Test.")
        reference_ngrams = [_create_ngrams([token.lemma_ for token in sentence], n=2)
                            for sentence in reference_doc.sents]
        reference_sentences = [sentence.text for sentence in reference_doc.sents]

        expected_result = RelevantSentence("Er besteht aus mehreren Tests.", 0.6, 1/3)
        self.assertEqual(expected_result, max_rouge_2_match(extracted_sentence, reference_sentences, reference_ngrams))


if __name__ == '__main__':
    unittest.main()
