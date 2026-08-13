"""Watched-episode tracking used by the library view."""

from aniworld.web import db


def test_marking_an_episode_watched():
    db.set_watched("Naruto", 1, 1, True)
    assert db.watched_for_title("Naruto") == [["1", 1]]


def test_marking_the_same_episode_watched_twice_does_not_duplicate():
    db.set_watched("Naruto", 1, 1, True)
    db.set_watched("Naruto", 1, 1, True)
    assert db.watched_for_title("Naruto") == [["1", 1]]


def test_unmarking_an_episode():
    db.set_watched("Naruto", 1, 1, True)
    db.set_watched("Naruto", 1, 1, False)
    assert db.watched_for_title("Naruto") == []


def test_unmarking_something_never_marked_is_a_no_op():
    db.set_watched("Naruto", 1, 1, False)
    assert db.watched_for_title("Naruto") == []


def test_watched_episodes_are_scoped_to_their_title():
    db.set_watched("Naruto", 1, 1, True)
    db.set_watched("One Piece", 1, 1, True)
    assert db.watched_for_title("Naruto") == [["1", 1]]


def test_the_same_season_and_episode_in_different_custom_paths_are_independent():
    db.set_watched("Naruto", 1, 1, True, custom_path_id=1)
    assert db.watched_for_title("Naruto", custom_path_id=1) == [["1", 1]]
    assert db.watched_for_title("Naruto", custom_path_id=2) == []


def test_the_same_season_and_episode_in_different_language_folders_are_independent():
    db.set_watched("Naruto", 1, 1, True, lang_folder="german-dub")
    assert db.watched_for_title("Naruto", lang_folder="german-dub") == [["1", 1]]
    assert db.watched_for_title("Naruto", lang_folder="german-sub") == []


def test_multiple_watched_episodes_of_one_title():
    db.set_watched("Naruto", 1, 1, True)
    db.set_watched("Naruto", 1, 2, True)
    db.set_watched("Naruto", 2, 1, True)
    assert sorted(db.watched_for_title("Naruto")) == [["1", 1], ["1", 2], ["2", 1]]
