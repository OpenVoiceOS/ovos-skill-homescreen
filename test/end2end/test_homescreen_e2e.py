"""End-to-end (ovoscope) tests for ovos-skill-homescreen.

The homescreen skill has no spoken intents — it is a resting-screen provider
driven by bus events. These tests exercise that bus contract in a real
MiniCroft (in-process SkillManager on a FakeBus):

- it registers itself with the homescreen manager on load / reload
- activating its display triggers the resting-screen handler, which announces
  ``ovos.homescreen.displayed``

GUI messages are ignored (ovoscope does not assert GUI rendering).
"""
from unittest import TestCase

from ovos_bus_client.message import Message
from ovos_bus_client.session import Session
from ovos_utils.log import LOG
from ovoscope import End2EndTest, CaptureSession, get_minicroft

SKILL_ID = "ovos-skill-homescreen.openvoiceos"


class TestHomescreenE2E(TestCase):
    def setUp(self):
        LOG.set_level("CRITICAL")
        self.minicroft = get_minicroft([SKILL_ID])

    def tearDown(self):
        if self.minicroft:
            self.minicroft.stop()

    def test_skill_loads(self):
        # the skill is loaded into the running MiniCroft
        self.assertIn(SKILL_ID, self.minicroft.skill_ids)

    def _session_msg(self, msg_type, data=None):
        session = Session("test-session")
        session.lang = "en-US"
        return Message(msg_type, data or {},
                       context={"session": session.serialize(),
                                "source": "A", "destination": "B"})

    def test_registers_with_homescreen_manager(self):
        # on a manager reload the skill re-announces itself
        source = self._session_msg("homescreen.manager.reload.list")
        test = End2EndTest(
            minicroft=self.minicroft,
            skill_ids=[SKILL_ID],
            source_message=source,
            expected_messages=[
                source,
                Message("homescreen.manager.add",
                        {"name": "OVOSHomescreen", "id": SKILL_ID}),
            ],
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
        # set of messages (weather/notification requests depending on config),
        # so assert membership rather than an exact ordered sequence.
        src = self._session_msg("homescreen.manager.activate.display",
                                {"homescreen_id": SKILL_ID})
        session = CaptureSession(self.minicroft,
                                 eof_msgs=["ovos.homescreen.displayed"])
        session.capture(src, timeout=15)
        messages = session.finish()
        self.assertTrue(
            any(m.msg_type == "ovos.homescreen.displayed" for m in messages),
            "resting-screen handler did not emit 'ovos.homescreen.displayed'",
        )
