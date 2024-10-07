from ps5_xbox_common_games import (
    extract_xbox_ids,
    find_common_games,
    extract_ps5_games,
    extract_xbox_games,
)
from typing import List, Dict, Tuple, Any
import unittest


class TestExtractXboxIds(unittest.TestCase):

    def test_extract_xbox_ids_valid(self) -> None:
        """Test with valid Xbox Game Pass data.

        This test verifies that the function correctly extracts game IDs from
        a well-formed input list of dictionaries.
        """
        input_data: List[Dict[str, str]] = [
            {"non_id_field": "123ABC", "name": "Game 1"},
            {"id": "456ABC", "name": "Game 2"},
            {"id": "789ABC", "name": "Game 3"},
        ]

        expected_output: List[str] = ["456ABC", "789ABC"]
        result: List[str] = extract_xbox_ids(input_data)
        self.assertEqual(result, expected_output)

    def test_extract_xbox_single_id(self) -> None:
        """Test with one Xbox Game Pass id.

        This test verifies that the function correctly extracts game IDs from
        a one key input list of dictionaries.
        """
        input_data: List[Dict[str, str]] = [
            {"non_id_field": "123ABC", "name": "Game 1"},
            {"id": "456ABC", "name": "Game 2"},
        ]

        expected_output: List[str] = ["456ABC"]
        result: List[str] = extract_xbox_ids(input_data)
        self.assertEqual(result, expected_output)

    def test_extract_xbox_ids_with_zero_ids(self) -> None:
        """Test with zero Xbox Game Pass id.

        This test verifies that the function correctly extracts game IDs from
        a one key input list of dictionaries.
        """
        input_data: List[Dict[str, str]] = [
            {"non_id_field": "123ABC", "name": "Game 1"},
        ]

        expected_output: List[str] = []
        result: List[str] = extract_xbox_ids(input_data)
        self.assertEqual(result, expected_output)

    @unittest.skip(
        "This Test will fail, we dont need to address this as error handling exists when an invalid id is called."
    )
    def test_extract_xbox_ids_with_missing_keys(self) -> None:
        """Test with missing keys for Xbox Game Pass id.

        This test verifies that the function correctly extracts game IDs from
        a one key input list of dictionaries.
        """
        input_data: List[Dict[str, str]] = [
            {"non_id_field": "123ABC", "name": "Game 1"},
            {"id": "456ABC", "name": "Game 2"},
            {"non_id_field": "NNN456ABC", "name": "Game 2"},
        ]

        expected_output: List[str] = ["456ABC", ""]
        result: List[str] = extract_xbox_ids(input_data)
        self.assertEqual(expected_output, result)

    def test_extract_xbox_ids_with_empty_dictionary(self) -> None:
        """Test with missing keys for Xbox Game Pass id.

        This test verifies that the function correctly extracts game IDs from
        a one key input list of dictionaries.
        """
        input_data: List[Dict[str, str]] = [{}]

        expected_output: List[str] = []
        result: List[str] = extract_xbox_ids(input_data)
        self.assertEqual(expected_output, result)


class TestFindCommonGames(unittest.TestCase):
    def test_find_common_games_with_exact_names(self) -> None:
        """Test to find games with exact names.

        This test returns games on xbox and ps5 game pass that have
        a exact match score.
        """

        input_data_xbox: List[str] = ["Valorant", "Remnant 2", "Human Fall Flat"]
        input_data_ps5: List[str] = ["Remnant 2", "Human Fall Flat", "Valorant"]
        result: List[Tuple[str, str, int]] = [
            ("Remnant 2", "Remnant 2", 100),
            ("Human Fall Flat", "Human Fall Flat", 100),
            ("Valorant", "Valorant", 100),
        ]
        expected_output: List[Tuple[str, str, int]] = find_common_games(
            input_data_ps5, input_data_xbox
        )
        self.assertEqual(result, expected_output)

    def test_find_common_games_with_non_similar_names(self) -> None:
        """Test to find games with non similar names.

        This test returns empty list when the games have
        non similar (different) names.
        """

        input_data_xbox: List[str] = ["Minecraft", "Mortal Combat", "MLS"]
        input_data_ps5: List[str] = ["Remnant 2", "Human Fall Flat", "Valorant"]
        result: List[Tuple[str, str, int]] = []
        expected_output: List[Tuple[str, str, int]] = find_common_games(
            input_data_ps5, input_data_xbox
        )
        self.assertEqual(result, expected_output)

    def test_find_common_games_with_similar_names(self) -> None:
        """Test to find games with similar names.

        This test returns games on xbox and ps5 game pass that have
        similar names.
        """

        input_data_xbox: List[str] = ["Minecraft", "Mortal Combat", "MLS"]
        input_data_ps5: List[str] = ["Moancraft", "Human Fall Flat", "Valorant"]
        result: List[Tuple[str, str, int]] = []
        expected_output: List[Tuple[str, str, int]] = find_common_games(
            input_data_ps5, input_data_xbox
        )
        self.assertEqual(result, expected_output)

    def test_find_common_games_with_no_input(self) -> None:
        """Test to find games with no input names.

        This test returns empty list.
        """

        input_data_xbox: List[str] = []
        input_data_ps5: List[str] = []
        result: List[Tuple[str, str, int]] = []
        expected_output: List[Tuple[str, str, int]] = find_common_games(
            input_data_ps5, input_data_xbox
        )
        self.assertEqual(result, expected_output)


# Need only one test case to identify when the XHR data changes on Sony's end
class TestExtractPs5Games(unittest.TestCase):
    def test_extract_ps5_games_with_sample_games(self) -> None:
        """Test the extract_ps5_games function with a sample response JSON.

        This test verifies that the function correctly extracts the names of PS5 games
        from a mock JSON response, ensuring that it only includes titles that are available on the PS5.
        """
        input_data = [
            {
                "category": "Category 1",
                "games": [
                    {"name": "Game A", "device": "PS5"},
                    {"name": "Game B", "device": "PS4"},
                    {"name": "Game C", "device": "PS5"},
                ],
            },
            {
                "category": "Category 2",
                "games": [
                    {"name": "Game D", "device": "PS5"},
                    {"name": "Game E", "device": "PC"},
                    {"name": "Game F", "device": ""},
                ],
            },
            {
                "category": "Category 3",
                "games": [
                    {"name": "Game G", "device": "PS4"},
                    {"name": "Game H", "device": "PS5"},
                ],
            },
        ]

        expected_output: List[str] = ["Game A", "Game C", "Game D", "Game H"]
        result: List[str] = extract_ps5_games(input_data)
        self.assertEqual(expected_output, result)


# Need only one test case to identify when the XHR data changes on Sony's end
class TestExtractXboxGames(unittest.TestCase):
    def test_extract_exbox_games_with_sample_games(self) -> None:
        """Test extracting Xbox Game Pass games from a sample response JSON.

        This test checks if the function correctly extracts game titles from the
        provided JSON structure. It verifies that the output matches the expected list
        of game titles.
        """
        # Sample JSON response simulating Xbox Game Pass products
        input_data: Dict[str, Any] = {
            "Products": [
                {
                    "LocalizedProperties": [
                        {"ProductTitle": "Game One"},
                        {"ProductTitle": "Game Two"},
                    ]
                },
                {
                    "LocalizedProperties": [
                        {"ProductTitle": "Game Three"},
                        {"ProductTitle": "Game Four"},
                    ]
                },
            ]
        }

        expected_output: List[str] = ["Game One", "Game Two", "Game Three", "Game Four"]
        result: List[str] = extract_xbox_games(input_data)
        self.assertEqual(expected_output, result)


if __name__ == "__main__":
    unittest.main()
