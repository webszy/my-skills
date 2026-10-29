"""Mechanical protocol tests with explicitly SYNTHETIC approval, source and receipts.

These tests do not run an Agent, authenticate a human, or implement a login system.
"""
import copy
from datetime import datetime, timedelta
import importlib.util
import json
import re
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'validate_cdf.py'
SPEC = importlib.util.spec_from_file_location('validate_cdf', SCRIPT)
v = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(v)
T0 = '2026-10-29T10:00:00+08:00'
SNAPSHOT = v.digest(b'synthetic source/configuration snapshot')


def fence(value, language='json'):
    body = json.dumps(value, ensure_ascii=False, indent=2) if language == 'json' else value
    return '```' + language + '\n' + body + '\n```\n'


def fixture_document():
    scope = {k: [] for k in v.SCOPE_KEYS}
    scope.update(in_scope=['Approved login flow'], will_change=['src/api.py', 'src/form.ts'],
                 will_not_change=['Authentication mechanism'],
                 acceptance_criteria=['The user can sign in through the login form.'])
    scope_text = 'Scope-Lock-Version: cdf-scope/v1\n' + '\n'.join(k + ': ' + json.dumps(scope[k]) for k in v.SCOPE_KEYS)
    checks = [dict(id='CHECK-API', kind='task', description='Approved API response and API tests pass.'),
              dict(id='CHECK-FORM', kind='task', description='Approved form submission checks pass.'),
              dict(id='CHECK-LOGIN', kind='product', description='The complete approved login flow succeeds.')]
    plan_parts = {heading: 'Synthetic approved ' + heading + '.\n' for heading in v.PLAN_HEADINGS}
    plan_parts['Scope Lock'] = fence(scope_text, 'yaml')
    plan_parts['Acceptance Criteria'] = fence(scope['acceptance_criteria'])
    plan_parts['Verification Strategy'] = fence(checks)
    plan_parts['Next Action'] = 'Save as Task\n'
    plan = '\n'.join('### ' + name + '\n' + body for name, body in plan_parts.items())
    tasks = []
    for index, check in enumerate(('CHECK-API', 'CHECK-FORM'), 1):
        tasks.append(dict(id='TASK-%03d' % index, name=check, goal='Approved local delivery',
                          depends_on=[] if index == 1 else ['TASK-001'],
                          scope_mapping=['Approved login flow'], write_scope=[scope['will_change'][index - 1]],
                          shared_contracts=[], implementation_notes=['Approved adapter'],
                          contributes_to=['AC-001'], task_verification=[check],
                          must_not_change=['Authentication mechanism'], assumptions_and_stop_conditions=[],
                          definition_status='READY'))
    sections = {
        'CDF Resume Contract': fence(dict(resume_path='CDF only', execution_authorized=False, progress_created_by_save=False)),
        'Approval Summary': fence('SYNTHETIC FIXTURE ONLY: API and form login, local checks and product integration check. Save?', 'text'),
        'Development Plan': plan,
        'Approval Record': fence(dict(user_statement='SYNTHETIC: approve this plan and Save as Task.', context='synthetic test turn',
                                     action='Save as Task', type='full', approved_items=scope['in_scope'], conditions=[], unapproved_items=[])),
        'Dependency Graph': fence({task['id']: task['depends_on'] for task in tasks}),
        'Task Definitions': fence(tasks),
        'Acceptance Mapping': fence({'AC-001': ['CHECK-LOGIN']}),
        'Scope Guard': fence(dict(result='checked', evidence='synthetic://scope-review')),
        'Future CDF Execution Constraints': 'Resume only through CDF after current authorization, integrity/history/drift checks. Preserve scope. Local checks then product checks, gate and final review.\n',
        'Compilation Gate Result': fence(dict(status='READY', task_count=2)),
        'Save Verification': fence(dict(status='verified', verified_at=T0)),
    }
    meta = dict(task_contract=v.TASK_CONTRACT, handoff_type='approved-tasking', status='tasking_ready', source='cdf',
                approval_state='approved', risk_level='Level L', workspace='/synthetic/workspace', source_branch='main',
                source_commit='synthetic-commit', source_worktree_state='clean', source_worktree_changes=[],
                save_drift_preflight='matched', save_drift_notes='none', scope_lock_sha256='draft',
                approval_record_sha256='draft', definition_sha256='draft', created_at=T0,
                approval_basis='summary', phase_scoped=False)
    return meta, sections


def render(meta, sections):
    return ('---\n' + '\n'.join(k + ': ' + json.dumps(value, ensure_ascii=False) for k, value in meta.items())
            + '\n---\n# Synthetic login fixture\n\n'
            + '\n'.join('## ' + name + '\n' + body for name, body in sections.items()))


def seal_draft(path, meta, sections):
    """Test-only fixture construction. Never called to repair an existing saved task."""
    path.write_text(render(meta, sections))
    for unused in range(2):
        hashes = v.parse_document(path, check_hashes=False)['hashes']
        meta.update(hashes)
        path.write_text(render(meta, sections))
    return v.parse_document(path)


def evidence(eid, check=None, kind='check', snapshot=SNAPSHOT):
    return dict(id=eid, kind=kind, source='synthetic://' + eid, result='PASS', snapshot=snapshot, check_id=check, valid=True)


def initial_progress(path, doc):
    return dict(progress_contract=v.PROGRESS_CONTRACT, task_path=str(path.resolve()), task_contract=v.TASK_CONTRACT,
                task_document_sha256=doc['document_sha256'], **doc['hashes'], overall_state='not_started',
                created_at=T0, updated_at=T0, completed_at=None, source_snapshot=SNAPSHOT,
                authorizations=[dict(id='AUTH-1', user_request='SYNTHETIC: continue this task', context='test current turn',
                                     task_path=str(path.resolve()), definition_sha256=doc['hashes']['definition_sha256'],
                                     action='Execute Saved Approved Scope')], events=[],
                tasks=[dict(id=tid, state='pending', verification_evidence=[]) for tid in doc['tasks']],
                evidence=[], completion_gate=None, final_review=None, completion_history=[])


def transition(progress, doc, tid, to, reopen=False):
    row = next(t for t in progress['tasks'] if t['id'] == tid)
    seq = len(progress['events']) + 1
    moment = (datetime.fromisoformat(progress['updated_at']) + timedelta(minutes=1)).isoformat()
    event = dict(seq=seq, task_id=tid, **{'from': row['state']}, to=to, at=moment, authorization='AUTH-1',
                 reason='Synthetic observed event', evidence=[], affected_tasks=[], scope_evidence=[], new_decisions=False)
    if reopen:
        event['reason'] = 'Synthetic regression disproves original verification, repair is within approved plan'
        affected = v.descendants(doc['tasks'], tid)
        event['affected_tasks'] = sorted(affected)
        eid = 'SCOPE-' + str(seq)
        progress['evidence'].append(evidence(eid, kind='scope_compliance'))
        event['scope_evidence'] = [eid]
        for task in progress['tasks']:
            if task['id'] in affected | {tid}:
                for item in progress['evidence']:
                    if item['id'] in task['verification_evidence']:
                        item['valid'] = False
                task['verification_evidence'] = []
                if task['id'] != tid and task['state'] != 'pending':
                    task['state'] = 'blocked'
        if progress['completion_gate']:
            progress['completion_history'].append(dict(completion_gate=progress['completion_gate'],
                                                       final_review=progress['final_review'], invalidated_reason=event['reason']))
            progress['completion_gate'] = progress['final_review'] = None
    if to == 'verified':
        for check in doc['tasks'][tid]['task_verification']:
            eid = check + '-' + str(seq)
            progress['evidence'].append(evidence(eid, check))
            event['evidence'].append(eid)
        row['verification_evidence'] = event['evidence'][:]
    row['state'] = to
    progress['events'].append(event)
    progress['updated_at'] = moment
    progress['overall_state'] = 'in_progress'
    progress['completed_at'] = None


def finish_tasks(progress, doc):
    for tid in doc['tasks']:
        transition(progress, doc, tid, 'in_progress')
        transition(progress, doc, tid, 'verified')


def complete(progress, doc):
    ev = [evidence('G-' + check, check) for check in doc['checks']]
    ev += [evidence('G-' + kind, kind=kind) for kind in ('agent_activity', 'diff_review', 'scope_compliance')]
    rows = [dict(check=check, required=True, result='PASS', command='synthetic ' + check,
                 working_directory='/synthetic', exit_code=0, reason='Synthetic check result', evidence=['G-' + check]) for check in doc['checks']]
    rows += [dict(check=category, required=False, result='NOT_APPLICABLE', command='synthetic inspection',
                  working_directory='/synthetic', exit_code=None, reason='Synthetic fixture has no such toolchain', evidence=['G-diff_review']) for category in ('tests', 'lint', 'typecheck', 'build')]
    gate_time = (datetime.fromisoformat(progress['updated_at']) + timedelta(minutes=1)).isoformat()
    review_time = (datetime.fromisoformat(gate_time) + timedelta(minutes=1)).isoformat()
    done_time = (datetime.fromisoformat(review_time) + timedelta(minutes=1)).isoformat()
    progress['completion_gate'] = dict(status='PASS', acceptance_criteria=[dict(criterion=ac, result='PASS', evidence=['G-CHECK-LOGIN']) for ac in doc['scope']['acceptance_criteria']],
                                       validation_results=rows, changed_files=[dict(path='src/api.py', change='Synthetic task output', evidence=['G-diff_review'])],
                                       out_of_scope_changes=[], known_issues=[], unverified_items=[], evidence=ev,
                                       source_snapshot=SNAPSHOT, evaluated_at=gate_time)
    progress['evidence'].append(evidence('FINAL', kind='final_review'))
    progress['final_review'] = dict(result='PASS', evidence=['FINAL'], source_snapshot=SNAPSHOT,
                                    reviewed_at=review_time, outstanding_findings=[],
                                    required_approval=False, approval_evidence=[])
    progress['overall_state'] = 'completed'
    progress['completed_at'] = progress['updated_at'] = done_time


class ProtocolTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'task.md'
        self.meta, self.sections = fixture_document()
        self.doc = seal_draft(self.path, self.meta, self.sections)
        self.progress = initial_progress(self.path, self.doc)

    def check_progress(self, previous=None, snapshot=None):
        return v.validate_progress(self.progress, self.doc, self.path, previous, snapshot)

    def invalid(self, callback, code):
        with self.assertRaises(v.Invalid) as caught:
            callback()
        self.assertEqual(caught.exception.code, code)

    def alter_section(self, name, mutate):
        obj = v.json_section(self.sections[name])
        mutate(obj)
        self.sections[name] = fence(obj)
        self.path.write_text(render(self.meta, self.sections))

    def completed(self):
        finish_tasks(self.progress, self.doc)
        complete(self.progress, self.doc)

    def test_valid_document_and_initial_progress(self):
        self.assertEqual(v.parse_document(self.path)['hashes'], self.doc['hashes'])
        self.assertEqual(set(self.check_progress().values()), {'pending'})

    def test_api_local_verified_unblocks_frontend_before_product_acceptance(self):
        transition(self.progress, self.doc, 'TASK-001', 'in_progress')
        transition(self.progress, self.doc, 'TASK-001', 'verified')
        transition(self.progress, self.doc, 'TASK-002', 'in_progress')
        self.assertEqual(self.check_progress()['TASK-002'], 'in_progress')
        self.assertIsNone(self.progress['completion_gate'])
        self.assertIsNone(self.progress['completed_at'])
        transition(self.progress, self.doc, 'TASK-002', 'verified')
        complete(self.progress, self.doc)
        self.check_progress()

    def test_frontend_cannot_start_before_api(self):
        transition(self.progress, self.doc, 'TASK-002', 'in_progress')
        self.invalid(self.check_progress, 'dependency-state')

    def test_definition_tamper_without_scope_change(self):
        before = self.path.read_text()
        self.path.write_text(before.replace('Synthetic approved Technical Approach.', 'Use an unapproved architecture.'))
        self.invalid(lambda: v.parse_document(self.path), 'integrity-mismatch')
        self.assertEqual(v.parse_document(self.path, False)['hashes']['scope_lock_sha256'], self.doc['hashes']['scope_lock_sha256'])

    def test_metadata_tamper_is_covered(self):
        self.path.write_text(self.path.read_text().replace('"main"', '"other-branch"'))
        self.invalid(lambda: v.parse_document(self.path), 'integrity-mismatch')

    def test_save_receipt_tamper_is_covered(self):
        self.path.write_text(self.path.read_text().replace('"verified_at": "' + T0, '"verified_at": "2026-10-29T10:01:00+08:00'))
        self.invalid(lambda: v.parse_document(self.path), 'integrity-mismatch')

    def test_task_implementation_tamper_is_covered(self):
        self.alter_section('Task Definitions', lambda ts: ts[0]['implementation_notes'].append('Unapproved new module'))
        self.invalid(lambda: v.parse_document(self.path), 'integrity-mismatch')

    def test_missing_definition_digest_not_bootstrapped(self):
        self.path.write_text('\n'.join(l for l in self.path.read_text().splitlines() if not l.startswith('definition_sha256:')) + '\n')
        before = self.path.read_bytes()
        self.invalid(lambda: v.parse_document(self.path), 'missing-field')
        self.assertEqual(before, self.path.read_bytes())

    def test_invalid_or_mismatched_digest(self):
        for value, code in [('Unavailable', 'digest'), ('0' * 64, 'integrity-mismatch')]:
            with self.subTest(value=value):
                self.meta['definition_sha256'] = value
                self.path.write_text(render(self.meta, self.sections))
                self.invalid(lambda: v.parse_document(self.path), code)

    def test_definition_digest_excludes_only_own_line(self):
        before = v.definition_bytes(self.path.read_bytes())
        self.meta['definition_sha256'] = '0' * 64
        self.path.write_text(render(self.meta, self.sections))
        self.assertEqual(before, v.definition_bytes(self.path.read_bytes()))
        self.meta['scope_lock_sha256'] = '0' * 64
        self.path.write_text(render(self.meta, self.sections))
        self.assertNotEqual(before, v.definition_bytes(self.path.read_bytes()))

    def test_hashes_match_independent_hashlib(self):
        import hashlib
        data = self.path.read_bytes()
        lines = data.splitlines(keepends=True)
        reference = b''.join(l for l in lines if not l.startswith(b'definition_sha256: '))
        self.assertEqual(hashlib.sha256(reference).hexdigest(), self.doc['hashes']['definition_sha256'])

    def test_v1_is_explicit_legacy(self):
        self.path.write_text(self.path.read_text().replace('cdf-cdtask/v2', 'cdf-cdtask/v1'))
        self.invalid(lambda: v.parse_document(self.path), 'legacy-reapproval')

    def test_unknown_contract(self):
        self.path.write_text(self.path.read_text().replace('cdf-cdtask/v2', 'cdf-cdtask/v99'))
        self.invalid(lambda: v.parse_document(self.path), 'contract-version')

    def test_duplicate_task_id(self):
        self.alter_section('Task Definitions', lambda ts: ts.append(copy.deepcopy(ts[0])))
        self.invalid(lambda: v.parse_document(self.path), 'duplicate-id')

    def test_missing_task_verification_field(self):
        self.alter_section('Task Definitions', lambda ts: ts[0].pop('task_verification'))
        self.invalid(lambda: v.parse_document(self.path), 'missing-field')

    def test_unknown_dependency(self):
        self.alter_section('Task Definitions', lambda ts: ts[0]['depends_on'].append('TASK-999'))
        self.alter_section('Dependency Graph', lambda g: g['TASK-001'].append('TASK-999'))
        self.invalid(lambda: v.parse_document(self.path), 'dependency')

    def test_dependency_cycle(self):
        self.alter_section('Task Definitions', lambda ts: ts[0]['depends_on'].append('TASK-002'))
        self.alter_section('Dependency Graph', lambda g: g['TASK-001'].append('TASK-002'))
        self.invalid(lambda: v.parse_document(self.path), 'cycle')

    def test_graph_projection_disagreement(self):
        self.alter_section('Dependency Graph', lambda g: g['TASK-002'].clear())
        self.invalid(lambda: v.parse_document(self.path), 'graph')

    def test_scope_key_order_rejected(self):
        self.path.write_text(self.path.read_text().replace('out_of_scope: []\nnon_goals: []', 'non_goals: []\nout_of_scope: []'))
        self.invalid(lambda: v.parse_document(self.path), 'scope-order')

    def test_empty_scope_rejected(self):
        self.path.write_text(self.path.read_text().replace('in_scope: ["Approved login flow"]', 'in_scope: []'))
        self.invalid(lambda: v.parse_document(self.path), 'empty')

    def test_noncanonical_task_scope_rejected(self):
        self.alter_section('Task Definitions', lambda ts: ts[0]['scope_mapping'].append('New product feature'))
        self.invalid(lambda: v.parse_document(self.path), 'scope')

    def test_exclusions_must_remain_protected(self):
        self.alter_section('Task Definitions', lambda ts: ts[0]['must_not_change'].clear())
        self.invalid(lambda: v.parse_document(self.path), 'scope')

    def test_task_cannot_add_new_verification_obligation(self):
        self.alter_section('Task Definitions', lambda ts: ts[0]['task_verification'].append('NEW-PRODUCT-REQUIREMENT'))
        self.invalid(lambda: v.parse_document(self.path), 'task-verification')

    def test_product_check_not_local_task_gate(self):
        self.alter_section('Task Definitions', lambda ts: ts[0].update(task_verification=['CHECK-LOGIN']))
        self.invalid(lambda: v.parse_document(self.path), 'task-verification')

    def test_missing_acceptance_mapping(self):
        self.alter_section('Acceptance Mapping', lambda m: m.clear())
        self.invalid(lambda: v.parse_document(self.path), 'missing-field')

    def test_extra_acceptance_mapping(self):
        self.alter_section('Acceptance Mapping', lambda m: m.update({'AC-002': ['CHECK-LOGIN']}))
        self.invalid(lambda: v.parse_document(self.path), 'unknown-field')

    def test_unknown_contribution(self):
        self.alter_section('Task Definitions', lambda ts: ts[0].update(contributes_to=['AC-009']))
        self.invalid(lambda: v.parse_document(self.path), 'acceptance-mapping')

    def test_save_cannot_authorize_execute(self):
        self.alter_section('CDF Resume Contract', lambda r: r.update(execution_authorized=True))
        self.invalid(lambda: v.parse_document(self.path), 'authorization')

    def test_approval_must_be_save(self):
        self.alter_section('Approval Record', lambda r: r.update(action='Execute Now'))
        self.invalid(lambda: v.parse_document(self.path), 'authorization')

    def test_runtime_requires_authorization(self):
        self.progress['authorizations'] = []
        self.invalid(self.check_progress, 'authorization')

    def test_inspect_and_save_cannot_be_runtime_authorization(self):
        for action in ('Inspect', 'Save as Task'):
            with self.subTest(action=action):
                self.progress['authorizations'][0]['action'] = action
                self.invalid(self.check_progress, 'authorization')

    def test_progress_bound_to_definition_and_path(self):
        self.progress['task_path'] += '.other'
        self.invalid(self.check_progress, 'binding')

    def test_illegal_transition(self):
        transition(self.progress, self.doc, 'TASK-001', 'verified')
        self.invalid(self.check_progress, 'transition')

    def test_projection_cannot_forge_verified(self):
        self.progress['tasks'][0]['state'] = 'verified'
        self.invalid(self.check_progress, 'state')

    def test_local_checks_required_for_verified(self):
        transition(self.progress, self.doc, 'TASK-001', 'in_progress')
        transition(self.progress, self.doc, 'TASK-001', 'verified')
        self.progress['evidence'][0]['check_id'] = 'CHECK-LOGIN'
        self.invalid(self.check_progress, 'task-verification')

    def test_controlled_reopen_preserves_history_and_invalidates_descendants(self):
        finish_tasks(self.progress, self.doc)
        old = copy.deepcopy(self.progress)
        transition(self.progress, self.doc, 'TASK-001', 'in_progress', reopen=True)
        self.check_progress(previous=old)
        self.assertEqual(self.progress['tasks'][1]['state'], 'blocked')
        self.assertFalse(self.progress['evidence'][0]['valid'])
        self.assertEqual(self.progress['events'][:4], old['events'])
        transition(self.progress, self.doc, 'TASK-001', 'verified')
        transition(self.progress, self.doc, 'TASK-002', 'in_progress')
        transition(self.progress, self.doc, 'TASK-002', 'verified')
        self.check_progress(previous=old)

    def test_reopen_missing_downstream_accounting(self):
        finish_tasks(self.progress, self.doc)
        transition(self.progress, self.doc, 'TASK-001', 'in_progress', reopen=True)
        self.progress['events'][-1]['affected_tasks'] = []
        self.invalid(self.check_progress, 'reopen')

    def test_reopen_must_invalidate_old_receipts(self):
        finish_tasks(self.progress, self.doc)
        transition(self.progress, self.doc, 'TASK-001', 'in_progress', reopen=True)
        self.progress['evidence'][0]['valid'] = True
        self.invalid(self.check_progress, 'reopen')

    def test_reopen_new_decision_rejected(self):
        finish_tasks(self.progress, self.doc)
        transition(self.progress, self.doc, 'TASK-001', 'in_progress', reopen=True)
        self.progress['events'][-1]['new_decisions'] = True
        self.invalid(self.check_progress, 'scope')

    def test_reopen_requires_scope_evidence(self):
        finish_tasks(self.progress, self.doc)
        transition(self.progress, self.doc, 'TASK-001', 'in_progress', reopen=True)
        self.progress['events'][-1]['scope_evidence'] = []
        self.invalid(self.check_progress, 'empty')

    def test_event_history_append_only(self):
        finish_tasks(self.progress, self.doc)
        previous = copy.deepcopy(self.progress)
        self.progress['events'][0]['reason'] = 'Rewritten history'
        self.invalid(lambda: self.check_progress(previous), 'history')

    def test_all_verified_without_product_gate_cannot_complete(self):
        finish_tasks(self.progress, self.doc)
        self.progress['overall_state'] = 'completed'
        self.invalid(self.check_progress, 'completion')

    def test_completed_requires_final_review_after_gate(self):
        self.completed()
        self.progress['final_review'] = None
        self.invalid(self.check_progress, 'completion')

    def test_completed_valid(self):
        self.completed()
        self.check_progress()

    def test_missing_product_criterion_prevents_completion(self):
        self.completed()
        self.progress['completion_gate']['acceptance_criteria'] = []
        self.invalid(self.check_progress, 'completion-coverage')

    def test_local_receipt_cannot_replace_product_check(self):
        self.completed()
        self.progress['completion_gate']['acceptance_criteria'][0]['evidence'] = ['G-CHECK-API']
        self.invalid(self.check_progress, 'completion-checks')

    def test_review_after_source_change_is_stale(self):
        self.completed()
        self.invalid(lambda: self.check_progress(snapshot=v.digest(b'changed source')), 'snapshot')

    def test_review_snapshot_must_match(self):
        self.completed()
        self.progress['final_review']['source_snapshot'] = v.digest(b'stale')
        self.invalid(self.check_progress, 'review')

    def test_review_must_follow_gate(self):
        self.completed()
        self.progress['final_review']['reviewed_at'] = T0
        self.invalid(self.check_progress, 'review')

    def test_pass_label_without_review_receipt_fails(self):
        self.completed()
        self.progress['final_review']['evidence'] = []
        self.invalid(self.check_progress, 'empty')

    def test_final_approval_only_when_required(self):
        self.completed()
        self.check_progress()
        self.progress['final_review']['required_approval'] = True
        self.invalid(self.check_progress, 'empty')

    def test_nonzero_exit_cannot_claim_pass(self):
        self.completed()
        self.progress['completion_gate']['validation_results'][0]['exit_code'] = 1
        self.invalid(self.check_progress, 'gate')

    def test_required_check_not_run_blocks_pass(self):
        self.completed()
        self.progress['completion_gate']['validation_results'][0]['result'] = 'NOT_RUN'
        self.invalid(self.check_progress, 'gate')

    def test_missing_referenced_evidence(self):
        self.completed()
        self.progress['completion_gate']['acceptance_criteria'][0]['evidence'] = ['MISSING']
        self.invalid(self.check_progress, 'evidence-ref')

    def test_stale_check_snapshot(self):
        self.completed()
        self.progress['completion_gate']['evidence'][0]['snapshot'] = v.digest(b'old')
        self.invalid(self.check_progress, 'stale-evidence')

    def test_misbound_validation_receipt(self):
        self.completed()
        self.progress['completion_gate']['validation_results'][0]['evidence'] = ['G-diff_review']
        self.invalid(self.check_progress, 'completion-checks')

    def test_unknown_progress_version_rejected(self):
        self.progress['progress_contract'] = 'cdf-execution-progress/v1'
        self.invalid(self.check_progress, 'progress-version')

    def test_duplicate_json_keys_rejected(self):
        self.invalid(lambda: v.strict_json('{"a":1,"a":2}'), 'duplicate-key')

    def test_nonfinite_json_rejected(self):
        self.invalid(lambda: v.strict_json('{"a":NaN}'), 'json')

    def test_crlf_rejected_without_normalization(self):
        self.path.write_bytes(self.path.read_bytes().replace(b'\n', b'\r\n'))
        self.invalid(lambda: v.parse_document(self.path), 'encoding')

    def test_duplicate_frontmatter_key(self):
        self.path.write_text(self.path.read_text().replace('source: "cdf"', 'source: "cdf"\nsource: "cdf"'))
        self.invalid(lambda: v.parse_document(self.path), 'duplicate-key')

    def test_embedded_approval_headings_are_not_sections(self):
        self.sections['Approval Summary'] = '````text\nSYNTHETIC\n## Development Plan\n```text\nquoted\n```\n````\n'
        seal_draft(self.path, self.meta, self.sections)

    def test_completed_reopen_archives_gate_and_review(self):
        self.completed()
        previous = copy.deepcopy(self.progress)
        transition(self.progress, self.doc, 'TASK-001', 'in_progress', reopen=True)
        self.check_progress(previous)
        self.assertEqual(self.progress['completion_history'][0]['final_review'], previous['final_review'])
        self.assertIsNone(self.progress['completed_at'])
        transition(self.progress, self.doc, 'TASK-001', 'verified')
        transition(self.progress, self.doc, 'TASK-002', 'in_progress')
        transition(self.progress, self.doc, 'TASK-002', 'verified')
        # The next review uses a new immutable receipt ID.
        complete(self.progress, self.doc)
        self.progress['evidence'][-1]['id'] = 'FINAL-2'
        self.progress['final_review']['evidence'] = ['FINAL-2']
        self.check_progress(previous)

    def test_reopen_cannot_keep_old_gate_even_on_same_source_snapshot(self):
        self.completed()
        old_gate = copy.deepcopy(self.progress['completion_gate'])
        transition(self.progress, self.doc, 'TASK-001', 'in_progress', reopen=True)
        self.progress['completion_gate'] = old_gate
        self.invalid(self.check_progress, 'stale-gate')

    def test_reopen_cannot_delete_completion_history(self):
        self.completed()
        previous = copy.deepcopy(self.progress)
        transition(self.progress, self.doc, 'TASK-001', 'in_progress', reopen=True)
        self.progress['completion_history'] = []
        self.invalid(lambda: self.check_progress(previous), 'history')

    def test_failure_takes_precedence_over_missing_evidence(self):
        self.completed()
        self.progress['completion_gate']['status'] = 'INSUFFICIENT_EVIDENCE'
        self.progress['completion_gate']['acceptance_criteria'][0]['result'] = 'FAIL'
        self.invalid(self.check_progress, 'gate')

    def test_runtime_identity_cannot_be_rewritten(self):
        previous = copy.deepcopy(self.progress)
        self.progress['created_at'] = '2026-10-29T09:59:00+08:00'
        self.invalid(lambda: self.check_progress(previous), 'history')

    def test_full_plan_approval_without_invented_summary(self):
        self.meta['approval_basis'] = 'full-plan'
        del self.sections['Approval Summary']
        seal_draft(self.path, self.meta, self.sections)

    def test_partial_approval_preserves_excluded_remainder(self):
        approval = v.json_section(self.sections['Approval Record'])
        approval.update(type='partial', unapproved_items=['Authentication mechanism'])
        self.sections['Approval Record'] = fence(approval)
        items = list(self.sections.items())
        items.insert(4, ('Partial Approval Result', fence(dict(approved_items=approval['approved_items'], unapproved_items=approval['unapproved_items']))))
        self.sections = dict(items)
        seal_draft(self.path, self.meta, self.sections)
        self.alter_section('Partial Approval Result', lambda obj: obj['approved_items'].append('New feature'))
        self.invalid(lambda: v.parse_document(self.path), 'partial')

    def test_phase_scope_and_deferred_protection(self):
        self.meta.update(risk_level='Level XL', phase_scoped=True)
        items = list(self.sections.items())
        items.insert(3, ('Approved Phase Boundary', fence(dict(phase='Phase 1', scope=['Approved login flow'], ends_at='Approved integration succeeds', explicitly_deferred=['Authentication mechanism']))))
        self.sections = dict(items)
        seal_draft(self.path, self.meta, self.sections)
        self.alter_section('Approved Phase Boundary', lambda obj: obj['scope'].append('New feature'))
        self.invalid(lambda: v.parse_document(self.path), 'phase')

    def test_missing_second_ac_contribution_detected(self):
        plan = self.sections['Development Plan']
        old_ac = ['The user can sign in through the login form.']
        new_ac = old_ac + ['The approved error is shown on rejected login.']
        plan = plan.replace('acceptance_criteria: ' + json.dumps(old_ac), 'acceptance_criteria: ' + json.dumps(new_ac))
        plan = plan.replace(fence(old_ac), fence(new_ac))
        self.sections['Development Plan'] = plan
        self.sections['Acceptance Mapping'] = fence({'AC-001': ['CHECK-LOGIN'], 'AC-002': ['CHECK-LOGIN']})
        self.path.write_text(render(self.meta, self.sections))
        self.invalid(lambda: v.parse_document(self.path, False), 'acceptance-coverage')

    def test_mapping_order_is_canonical(self):
        old_ac = ['The user can sign in through the login form.']
        new_ac = old_ac + ['The approved error is shown on rejected login.']
        self.sections['Development Plan'] = self.sections['Development Plan'].replace('acceptance_criteria: ' + json.dumps(old_ac), 'acceptance_criteria: ' + json.dumps(new_ac)).replace(fence(old_ac), fence(new_ac))
        self.alter_section('Task Definitions', lambda ts: ts[1]['contributes_to'].append('AC-002'))
        self.sections['Acceptance Mapping'] = fence({'AC-002': ['CHECK-LOGIN'], 'AC-001': ['CHECK-LOGIN']})
        self.path.write_text(render(self.meta, self.sections))
        self.invalid(lambda: v.parse_document(self.path, False), 'acceptance-mapping')

    def test_cli_read_only_json_status_and_errors(self):
        before = self.path.read_bytes()
        result = subprocess.run([sys.executable, str(SCRIPT), str(self.path)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        output = json.loads(result.stdout)
        self.assertEqual(output['mechanical_status'], 'VALID')
        self.assertFalse(output['execution_authorized'])
        self.assertTrue(output['review_required'])
        self.assertEqual(before, self.path.read_bytes())
        self.assertEqual(list(self.path.parent.iterdir()), [self.path])
        self.path.write_text(before.decode().replace('Synthetic approved Risks.', 'Tampered risks.'))
        result = subprocess.run([sys.executable, str(SCRIPT), str(self.path)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)['errors'][0]['code'], 'integrity-mismatch')

    def test_draft_hash_mode_explicitly_not_validated_integrity(self):
        result = subprocess.run([sys.executable, str(SCRIPT), str(self.path), '--draft-hashes'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)['mechanical_status'], 'DRAFT_HASHES_ONLY')

    def test_cli_malformed_input_has_json_error_no_traceback(self):
        self.path.write_text('not a task\n')
        result = subprocess.run([sys.executable, str(SCRIPT), str(self.path)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)['mechanical_status'], 'INVALID')
        self.assertEqual(result.stderr, '')


class PackageTests(unittest.TestCase):
    def test_local_document_links_and_heading_targets(self):
        root = SCRIPT.parents[1]
        files = list(root.rglob('*.md')) + [root.parents[1] / 'README.md', root.parents[1] / 'README.zh-CN.md']
        checked = 0
        for path in files:
            for target in re.findall(r'\[[^\]\n]+\]\(([^)]+)\)', path.read_text()):
                if '://' in target:
                    continue
                relative, _, anchor = target.partition('#')
                destination = (path.parent / relative).resolve() if relative else path
                with self.subTest(file=str(path), target=target):
                    self.assertTrue(destination.exists(), str(destination))
                    if anchor:
                        headings = re.findall(r'^#{1,6} (.+)$', destination.read_text(), re.M)
                        slugs = [re.sub(r'[^\w\- ]', '', h.lower()).replace(' ', '-') for h in headings]
                        self.assertIn(anchor, slugs)
                checked += 1
        self.assertGreater(checked, 50)

    def test_metadata_and_minimal_skill_frontmatter(self):
        root = SCRIPT.parents[1]
        package = json.loads((root / 'skill.json').read_text())
        collection = json.loads((root.parents[1] / 'skill.json').read_text())
        self.assertEqual(package['version'], '1.3.0')
        self.assertEqual(collection['version'], package['version'])
        self.assertEqual(next(s['version'] for s in collection['skills'] if s['name'] == 'cdf'), package['version'])
        for name in package['references'] + package['scripts'] + [package['entry']]:
            self.assertTrue((root / name).is_file(), name)
        text = (root / 'SKILL.md').read_text()
        self.assertLess(len(text.splitlines()), 500)
        self.assertTrue(text.startswith('---\n'))
        front = text.split('---\n', 2)[1]
        fields = dict(line.split(': ', 1) for line in front.splitlines())
        self.assertEqual(set(fields), {'name', 'description'})
        self.assertEqual(fields['name'], 'cdf')
        self.assertTrue(0 < len(fields['description']) < 1024)
        self.assertNotIn('[TODO:', text)
        # This package's two plain scalar fields are checked without a YAML dependency.
        self.assertNotIn(': ', fields['description'])
        self.assertIn('allow_implicit_invocation: false', (root / 'agents/openai.yaml').read_text())
        for name in ('README.md', 'README.zh-CN.md'):
            self.assertIn('1.3.0', (root / name).read_text())
            self.assertIn('v0.1', (root / name).read_text())


if __name__ == '__main__':
    unittest.main()
