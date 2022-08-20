from uuid import uuid4

import pytest

from app.db.models import Card
from app.tests.helpers import ABOUT_NOW, TestBasePersistent

NAMES = [
    "owner",
    "alice",
    "bob",
    "charlie",
    "david",
    "emily",
    "frank",
    "george",
    "heather",
]
CARDS = [
    "Black Lotus",
    "Ancestral Recall",
    "Mox Sapphire",
    "Mox Jet",
    "Mox Ruby",
    "Sol Ring",
    "Time Vault",
    "Mox Pearl",
    "Mox Emerald",
    "Tinker",
    "Karn, the Great Creator",
    "Time Walk",
    "Demonic Tutor",
    "Oko, Theif of Crowns",
    "Snapcaster Mage",
    "Force of Will",
]


class TestDraft(TestBasePersistent):
    @pytest.fixture(scope="class")
    def users_with_clients(self, user_and_client_factory):
        tuples = [user_and_client_factory({"username": username}) for username in NAMES]
        for user, client in tuples:
            user.client = client
        return [user for user, _ in tuples]

    @pytest.fixture(scope="class")
    def drafters(self, users_with_clients):
        return users_with_clients[1:]

    @pytest.fixture(scope="class")
    def cards_dict(self, db_session):
        ret = {}
        for card_name in CARDS:
            card = Card.from_dict(
                {
                    "name": card_name,
                    "vrd_legal": True,
                    "oracle_id": str(uuid4()),
                    "image_uri": f"image/{card_name}",
                }
            )
            db_session.add(card)
            ret[card_name] = card
        db_session.commit()
        return ret

    @pytest.fixture
    def draft_id(self, request):
        val = request.config.cache.get("TestDraft_shared_draft_id", None)
        if not val:
            raise ValueError
        return val

    @pytest.fixture
    def save_draft_id(self, request):
        def saver(val):
            request.config.cache.set("TestDraft_shared_draft_id", val)

        return saver

    def test_create_draft(self, owner, no_session_client, save_draft_id):
        resp = no_session_client.post(
            "api/drafts/new", json={"name": "test draft", "rounds": 3, "seats": 8}
        )
        assert resp.status_code == 401

        resp = owner.client.post(
            "api/drafts/new",
            json={
                "name": "test draft",
                "rounds": 3,
                "seats": 8,
                "random_seats": False,
            },
        )
        assert resp.status_code == 201
        save_draft_id(resp.json["id"])
        assert resp.json == {
            "id": resp.json["id"],
            "name": "test draft",
            "owner": {
                "id": owner.id,
                "username": owner.username,
            },
            "players": [],
            "picks": [],
            "preloads": [],
            "picks_completed": 0,
            "seats": 8,
            "rounds": 3,
            "multiseat": False,
            "random_seats": False,
            "created_at": ABOUT_NOW,
            "started_at": None,
            "pick_order": "snake",
            "format": "VRD",
        }

    @pytest.fixture
    def check_seats(self, owner, draft_id):
        def checker(*expected):
            get_resp = owner.client.get(f"api/drafts/{draft_id}")
            assert get_resp.status_code == 200
            assert [
                (seat["seat_no"], seat["player"]["username"]) for seat in get_resp.json["players"]
            ] == [(n, player.username) for n, player in expected]

        return checker

    def test_join(self, alice, bob, no_session_client, draft_id, check_seats):
        join_url = f"api/drafts/{draft_id}/join"

        resp = no_session_client.post(join_url, json={})
        assert resp.status_code == 401

        resp = alice.client.post(join_url, json={})
        assert resp.status_code == 201
        assert resp.json == {
            "id": resp.json["id"],
            "seat_no": 0,
            "player": {"id": alice.id, "username": alice.username},
        }

        resp = bob.client.post(join_url, json={})
        assert resp.status_code == 201
        assert resp.json["seat_no"] == 1
        assert resp.json["player"]["username"] == bob.username

        check_seats((0, alice), (1, bob))

    def test_join_twice_not_allowed(self, draft_id, alice, bob):
        join_url = f"api/drafts/{draft_id}/join"
        resp = alice.client.post(join_url, json={})
        assert resp.status_code == 409
        assert resp.json == {"error": "You already joined this draft"}
        resp = bob.client.post(join_url, json={"seat_no": 3})
        assert resp.status_code == 409
        assert resp.json == {"error": "You already joined this draft"}

    def test_join_filled_seat(self, charlie, draft_id):
        resp = charlie.client.post(f"api/drafts/{draft_id}/join", json={"seat_no": 0})
        assert resp.status_code == 409
        assert resp.json == {"error": "Seat is already filled"}

    def test_join_invalid_seat(self, charlie, draft_id):
        join_url = f"api/drafts/{draft_id}/join"
        resp = charlie.client.post(join_url, json={"seat_no": 8})
        assert resp.status_code == 422
        assert resp.json == {"errors": {"seat_no": "Must be less than 8"}}
        resp = charlie.client.post(join_url, json={"seat_no": -1})
        assert resp.status_code == 422
        assert resp.json == {"errors": {"seat_no": "value is less than 0"}}

    def test_join_seat_filling(self, drafters, check_seats, draft_id):
        join_url = f"api/drafts/{draft_id}/join"
        alice, bob, charlie, david, emily, frank, george, heather = drafters

        resp = heather.client.post(join_url, json={"seat_no": 7})
        assert resp.status_code == 201
        assert resp.json["seat_no"] == 7
        assert resp.json["player"]["username"] == heather.username

        charlie.client.post(join_url, json={})
        check_seats((0, alice), (1, bob), (2, charlie), (7, heather))

        emily.client.post(join_url, json={"seat_no": 4})
        david.client.post(join_url, json={})
        frank.client.post(join_url, json={})
        george.client.post(join_url, json={})
        check_seats(*enumerate(drafters))

    def test_join_full(self, owner, draft_id):
        resp = owner.client.post(f"api/drafts/{draft_id}/join", json={})
        assert resp.status_code == 409
        assert resp.json == {"error": "Draft is full"}

    def test_no_picks_before_start(self, alice, draft_id, ancestral_recall):
        resp = alice.client.post(
            f"api/drafts/{draft_id}/pick",
            json={"pick_no": 0, "card_id": ancestral_recall.oracle_id},
        )
        assert resp.status_code == 409
        assert resp.json == {"error": "Draft is not started"}

    def test_start(self, owner, alice, draft_id):
        resp = alice.client.post(f"api/drafts/{draft_id}/start")
        assert resp.status_code == 403
        assert resp.json == {"error": "Only the owner can start the draft"}

        resp = owner.client.post(f"api/drafts/{draft_id}/start")
        assert resp.status_code == 200
        assert resp.json["started_at"] == ABOUT_NOW

    def test_pick(self, alice, draft_id, ancestral_recall):
        resp = alice.client.post(
            f"api/drafts/{draft_id}/pick",
            json={"pick_no": 3, "card_id": ancestral_recall.oracle_id},
        )
        assert resp.status_code == 403
        assert resp.json == {"error": "You cannot make picks for seats that are not yours"}

        resp = alice.client.post(
            f"api/drafts/{draft_id}/pick",
            json={"pick_no": 0, "card_id": ancestral_recall.oracle_id},
        )
        assert resp.status_code == 201
        assert (
            resp.json["picks"][0]["card_name"] == ancestral_recall.name
        )  # TODO decide if this should be a dict instead or not

    def test_preload(self, bob, charlie, owner, draft_id, mox_sapphire, black_lotus):
        resp = charlie.client.post(
            f"api/drafts/{draft_id}/pick",
            json={"pick_no": 2, "card_id": mox_sapphire.oracle_id},
        )
        assert resp.status_code == 201
        assert len(resp.json["preloads"])
        assert resp.json["preloads"][0] == {
            "card_name": mox_sapphire.name,
            "card_id": mox_sapphire.oracle_id,
            "card_img": mox_sapphire.image_uri,
            "seat_id": resp.json["players"][2]["id"],
            "pick_no": 2,
            "round": 0,
        }

        # only charlie can see his preloads
        assert len(bob.client.get(f"api/drafts/{draft_id}").json["preloads"]) == 0
        assert len(charlie.client.get(f"api/drafts/{draft_id}").json["preloads"]) == 1
        assert len(owner.client.get(f"api/drafts/{draft_id}").json["preloads"]) == 0

        # preloads are automatically finalized when next to pick
        resp = bob.client.post(
            f"api/drafts/{draft_id}/pick",
            json={"pick_no": 1, "card_id": black_lotus.oracle_id},
        )
        assert resp.status_code == 201
        assert len(resp.json["picks"]) == 3

        assert len(charlie.client.get(f"api/drafts/{draft_id}").json["preloads"]) == 0

    def test_preload_sniped(self, draft_id, david, emily, mox_jet, black_lotus, mox_ruby):
        resp = emily.client.post(
            f"api/drafts/{draft_id}/pick",
            json={"pick_no": 4, "card_id": mox_jet.oracle_id},
        )
        assert resp.status_code == 201
        assert len(resp.json["preloads"]) == 1

        # previously picked cards are allowed, but aren't finalized.
        resp = david.client.post(
            f"api/drafts/{draft_id}/pick",
            json={"pick_no": 3, "card_id": black_lotus.oracle_id},
        )
        assert resp.status_code == 201
        assert len(resp.json["picks"]) == 3
        assert len(resp.json["preloads"]) == 1

        # make a real pick
        resp = david.client.post(
            f"api/drafts/{draft_id}/pick",
            json={"pick_no": 3, "card_id": mox_jet.oracle_id},
        )
        assert resp.status_code == 201
        assert len(resp.json["picks"]) == 4
        assert len(resp.json["preloads"]) == 0

        # emily got sniped
        assert len(emily.client.get(f"api/drafts/{draft_id}").json["preloads"]) == 1
        # she picks again
        resp = emily.client.post(
            f"api/drafts/{draft_id}/pick",
            json={"pick_no": 4, "card_id": mox_ruby.oracle_id},
        )
        assert resp.status_code == 201
        assert len(resp.json["picks"]) == 5
        assert len(resp.json["preloads"]) == 0

    def test_multiple_preloads(  # pylint: disable=too-many-arguments
        self,
        frank,
        george,
        heather,
        draft_id,
        sol_ring,
        time_vault,
        mox_pearl,
        mox_emerald,
        black_lotus,
        tinker,
    ):
        # you can preload far in the future, and it being already picked won't affect other preloads
        resp = heather.client.post(
            f"api/drafts/{draft_id}/pick",
            json={"pick_no": 23, "card_id": black_lotus.oracle_id},
        )
        assert resp.status_code == 201
        assert len(resp.json["preloads"]) == 1
        # more reasonable picks
        resp = heather.client.post(
            f"api/drafts/{draft_id}/pick",
            json={"pick_no": 8, "card_id": mox_emerald.oracle_id},
        )
        assert resp.status_code == 201
        assert len(resp.json["preloads"]) == 2
        resp = heather.client.post(
            f"api/drafts/{draft_id}/pick",
            json={"pick_no": 7, "card_id": mox_pearl.oracle_id},
        )
        assert resp.status_code == 201
        assert len(resp.json["preloads"]) == 3

        resp = george.client.post(
            f"api/drafts/{draft_id}/pick",
            json={"pick_no": 6, "card_id": time_vault.oracle_id},
        )
        assert resp.status_code == 201
        assert len(resp.json["preloads"]) == 1
        resp = george.client.post(
            f"api/drafts/{draft_id}/pick",
            json={"pick_no": 9, "card_id": tinker.oracle_id},
        )
        assert resp.status_code == 201
        assert len(resp.json["preloads"]) == 2

        # now frank sets off the chain reaction
        assert len(resp.json["picks"]) == 5
        resp = frank.client.post(
            f"api/drafts/{draft_id}/pick",
            json={"pick_no": 5, "card_id": sol_ring.oracle_id},
        )
        assert resp.status_code == 201
        assert len(resp.json["picks"]) == 10

        assert len(george.client.get(f"api/drafts/{draft_id}").json["preloads"]) == 0
        assert (
            len(heather.client.get(f"api/drafts/{draft_id}").json["preloads"]) == 1
        )  # black lotus

    def test_multiseat(self, alice, bob):
        resp = alice.client.post(
            "api/drafts/new",
            json={
                "name": "multiseat test draft",
                "rounds": 2,
                "seats": 2,
                "multiseat": True,
            },
        )
        assert resp.status_code == 201
        multiseat_draft_id = resp.json["id"]
        assert resp.json["multiseat"] is True

        resp = bob.client.post(f"api/drafts/{multiseat_draft_id}/join", json={})
        assert resp.status_code == 201
        resp = bob.client.post(f"api/drafts/{multiseat_draft_id}/join", json={})
        assert resp.status_code == 201

        resp = alice.client.get(f"api/drafts/{multiseat_draft_id}")
        assert [seat["player"]["username"] for seat in resp.json["players"]] == [
            "bob",
            "bob",
        ]

        # TODO check preloads

    def test_random_seats(self):
        pass  # TODO

    def test_list(self):
        pass  # TODO


# Generate some more specific fixtures programmatically.
# `idx=i`/`card_nm=name` effectively captures by value instead of reference
for i, name in enumerate(NAMES):

    @pytest.fixture(scope="class")
    def user_fixture(_self, users_with_clients, idx=i):
        return users_with_clients[idx]

    setattr(TestDraft, name, user_fixture)

for name in CARDS:

    @pytest.fixture(scope="class")
    def card_fixture(_self, cards_dict, card_nm=name):
        return cards_dict[card_nm]

    setattr(TestDraft, name.lower().replace(" ", "_").replace(",", ""), card_fixture)
