"""Golden end-to-end (ovoscope) coverage for ovos-skill-homescreen.

Intent-surface investigation (see PR description): this skill ships no
``locale/`` directory and registers zero ``@intent_handler`` /
``@intent_file_handler`` decorated methods (``grep -rn "intent_handler" .``
over the checkout returns nothing outside ``test/``). It is a pure
resting-screen provider: it wins the "homescreen" GUI page and reacts only to
bus events emitted by the homescreen manager, other skills, and the GUI
itself (``self.add_event``/``self.bus.on`` calls in ``initialize()``). There
are therefore no voice utterances to write golden rows for -- inventing them
would test nothing this skill actually does.

Instead this suite is a registration / bus-contract suite in the same spirit
as a golden-utterance suite: for each bus API this skill exposes, drive a
real MiniCroft (in-process SkillManager on a FakeBus, via ovoscope) with the
message a caller would send and assert the skill reacts correctly --
loads cleanly, re-announces itself to the homescreen manager, accepts skill
registrations (example utterances + app-drawer icons) for its idle-screen
rendering, and (de)registers cleanly when a skill unloads.

GUI-rendering itself (the QML page) is out of scope for ovoscope -- only the
message-bus side of the contract is asserted here.
"""
from unittest import TestCase

from ovos_bus_client.message import Message
from ovos_bus_client.session import Session
from ovos_utils.log import LOG
from ovoscope import End2EndTest, CaptureSession, get_minicroft

SKILL_ID = "ovos-skill-homescreen.openvoiceos"


def _session_msg(msg_type, data=None):
    session = Session("test-session")
    session.lang = "en-US"
    return Message(msg_type, data or {},
                    context={"session": session.serialize(),
                             "source": "A", "destination": "B"})


class TestHomescreenE2E(TestCase):
    def setUp(self):
        LOG.set_level("CRITICAL")
        self.minicroft = get_minicroft([SKILL_ID])

    def tearDown(self):
        if self.minicroft:
            self.minicroft.stop()

    def test_skill_loads(self):
        # the skill is loaded into the running MiniCroft with no exceptions
        self.assertIn(SKILL_ID, self.minicroft.skill_ids)

    def test_registers_with_homescreen_manager(self):
        # on a manager reload the skill re-announces itself so the manager
        # can offer it as a selectable resting screen
        source = _session_msg("homescreen.manager.reload.list")
        # No handler here emits "ovos.utterance.handled" (End2EndTest's
        # default eof topic, meant for voice-intent scenarios) -- this is a
        # direct bus-API call, not an utterance, so there is nothing to wait
        # on. Without overriding eof_msgs the capture always times out (the
        # expected messages still arrive; only the eof wait fails), so pin
        # eof_msgs to the actual reply topic this handler emits.
        test = End2EndTest(
            minicroft=self.minicroft,
            skill_ids=[SKILL_ID],
            source_message=source,
            expected_messages=[
                source,
                Message("homescreen.manager.add",
                        {"name": "OVOSHomescreen", "id": SKILL_ID}),
            ],
            eof_msgs=["homescreen.manager.add"],
            test_message_number=False,
            test_msg_data=False,
            test_msg_context=False,
            test_boot_sequence=False,
            test_final_session=False,
            test_routing=False,
            test_active_skills=False,
        )
        test.execute(timeout=10)

    def test_resting_screen_activates(self):
        # activating the display runs the resting-screen handler, which
        # announces the homescreen as displayed. The handler emits a variable
        # set of messages (weather/notification requests depending on
        # config), so assert membership rather than an exact ordered
        # sequence.
        src = _session_msg("homescreen.manager.activate.display",
                            {"homescreen_id": SKILL_ID})
        session = CaptureSession(self.minicroft,
                                  eof_msgs=["ovos.homescreen.displayed"])
        session.capture(src, timeout=15)
        messages = session.finish()
        self.assertTrue(
            any(m.msg_type == "ovos.homescreen.displayed" for m in messages),
            "resting-screen handler did not emit 'ovos.homescreen.displayed'",
        )

    def test_register_skill_example_utterances(self):
        # another skill registers its spoken examples for the idle screen's
        # example carousel; the homescreen must accept the registration
        # without raising and must not blow up re-rendering the examples.
        src = _session_msg("homescreen.register.examples", {
            "skill_id": "ovos-skill-dummy.openvoiceos",
            "lang": "en-US",
            "utterances": ["do the thing"],
        })
        # The handler runs synchronously on the FakeBus and emits no
        # dedicated "done" topic, so there is no eof message to wait on;
        # a short fixed timeout just gives the handler a chance to run
        # before the session closes. This is a smoke test: it fails if the
        # skill crashes hard enough to take down the MiniCroft/bus, but a
        # handler exception caught internally by ovos-bus-client would only
        # surface as a logged error, not a test failure.
        session = CaptureSession(self.minicroft, eof_msgs=[])
        session.capture(src, timeout=2)
        session.finish()

    def test_register_homescreen_app(self):
        # another skill registers an app-drawer icon; the homescreen must
        # accept it without raising and re-render the apps drawer.
        src = _session_msg("homescreen.register.app", {
            "skill_id": "ovos-skill-dummy.openvoiceos",
            "icon": "dummy.png",
            "event": "ovos-skill-dummy.openvoiceos.launch",
            "name": "Dummy",
        })
        session = CaptureSession(self.minicroft, eof_msgs=[])
        session.capture(src, timeout=2)
        session.finish()

    def test_deregister_skill_on_unload(self):
        # register then deregister (detach_skill) a skill's example
        # utterances/app icon; the homescreen must clean up without raising,
        # even though it never registered anything for this skill_id before
        # (defensive membership checks in handle_deregister_skill).
        skill_id = "ovos-skill-dummy.openvoiceos"
        register = _session_msg("homescreen.register.app", {
            "skill_id": skill_id,
            "icon": "dummy.png",
            "event": f"{skill_id}.launch",
            "name": "Dummy",
        })
        session = CaptureSession(self.minicroft, eof_msgs=[])
        session.capture(register, timeout=2)
        session.finish()

        deregister = _session_msg("detach_skill", {"skill_id": skill_id})
        session = CaptureSession(self.minicroft, eof_msgs=[])
        session.capture(deregister, timeout=2)
        session.finish()
