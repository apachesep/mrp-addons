# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp.tests import common


class TestCrmClaimCall(common.TransactionCase):

    def setUp(self):
        super(TestCrmClaimCall, self).setUp()
        self.crm_claim = self.env.ref('crm_claim.crm_claim_1')
        self.phonecall1 = self.env.ref('crm.crm_phonecall_1')
        self.wiz_model = self.env['crm.phonecall2phonecall']
        self.phonecall = self.env.ref('crm.crm_phonecall_4')
        self.claim = self.env.ref('crm_claim.crm_claim_2')
        self.phonecall_obj = self.env['crm.phonecall']

    def test_crm_claim(self):
        phonecalls = [(6, 0, [self.phonecall1.id])]
        self.crm_claim.phonecall_ids = phonecalls
        self.assertEqual(
            self.crm_claim.phonecalls_count, len(self.crm_claim.phonecall_ids),
            'Should be 1 phonecall')

    def test_onchange_claim(self):
        self.phonecall1.claim_id = self.crm_claim.id
        self.phonecall1.onchange_claim_id()
        self.assertEqual(self.crm_claim.partner_id, self.phonecall1.partner_id)

    def test_schedule_call_claim_id(self):
        self.phonecall.claim_id = self.claim.id
        fields = (
            ['action', 'name', 'partner_id', 'opportunity_ids', 'claim_id'])
        defaults = self.env['crm.phonecall2phonecall'].with_context(
            active_id=self.phonecall.id).default_get(fields)
        self.assertEqual(self.claim.id, defaults.get('claim_id'))
        wiz = self.wiz_model.create(defaults)
        res = wiz.with_context(
            active_ids=[self.phonecall.id]).action_schedule()
        self.assertEqual(self.claim.id,
                         self.phonecall_obj.browse(res['res_id']).claim_id.id)
