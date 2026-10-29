#!/usr/bin/env python3
"""Read-only CDF v2 mechanical validator. No command grants approval or executes work."""
import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path

TASK_CONTRACT = 'cdf-cdtask/v2'
PROGRESS_CONTRACT = 'cdf-execution-progress/v2'
SCOPE_KEYS = ['in_scope', 'out_of_scope', 'non_goals', 'assumptions',
              'stop_conditions', 'will_change', 'will_not_change', 'acceptance_criteria']
PLAN_HEADINGS = ['Requirement Understanding', 'Evidence Summary', 'Risk Gate Result',
                 'Scope Lock', 'Technical Approach', 'Implementation Plan', 'Risks',
                 'Rollback Plan', 'Acceptance Criteria', 'Verification Strategy', 'Next Action']
META_FIELDS = ['task_contract', 'handoff_type', 'status', 'source', 'approval_state',
               'risk_level', 'workspace', 'source_branch', 'source_commit',
               'source_worktree_state', 'source_worktree_changes', 'save_drift_preflight',
               'save_drift_notes', 'scope_lock_sha256', 'approval_record_sha256',
               'definition_sha256', 'created_at', 'approval_basis', 'phase_scoped']
TASK_FIELDS = ['id', 'name', 'goal', 'depends_on', 'scope_mapping', 'write_scope',
               'shared_contracts', 'implementation_notes', 'contributes_to',
               'task_verification', 'must_not_change', 'assumptions_and_stop_conditions',
               'definition_status']
GATE_FIELDS = ['status', 'acceptance_criteria', 'validation_results', 'changed_files',
               'out_of_scope_changes', 'known_issues', 'unverified_items', 'evidence',
               'source_snapshot', 'evaluated_at']
REVIEW_FIELDS = ['result', 'evidence', 'source_snapshot', 'reviewed_at',
                 'outstanding_findings', 'required_approval', 'approval_evidence']
TRANSITIONS = {'pending': ['in_progress'], 'in_progress': ['verified', 'blocked'],
               'blocked': ['in_progress'], 'verified': ['in_progress']}
SEMANTIC_REVIEW = [
    'Verify human approval provenance and current-turn action; a digest is not a signature.',
    'Compare the displayed approval basis, plan, phase, exclusions, task checks and write scopes.',
    'Inspect repository drift, historical progress attribution and read-only evidence dependencies.',
    'Open every evidence source, confirm actual results and current source/configuration bindings.',
    'Perform final scoped review and only the human approvals required by the approved workflow.',
]


class Invalid(ValueError):
    def __init__(self, code, message):
        self.code = code
        super().__init__(message)


def require(condition, code, message):
    if not condition:
        raise Invalid(code, message)


def strict_json(text):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'duplicate-key', key)
            result[key] = value
        return result
    def constant(value):
        raise Invalid('json', 'Non-finite JSON value: ' + value)
    try:
        return json.loads(text, object_pairs_hook=pairs, parse_constant=constant)
    except (json.JSONDecodeError, UnicodeError) as error:
        raise Invalid('json', str(error)) from error


def fields(value, names, where, exact=True):
    require(isinstance(value, dict), 'shape', where + ' must be an object')
    require(set(names) <= value.keys(), 'missing-field', where + ': ' + ', '.join(sorted(set(names) - value.keys())))
    if exact:
        require(set(names) == value.keys(), 'unknown-field', where + ': unknown fields')


def string(value, where):
    require(isinstance(value, str) and bool(value.strip()), 'shape', where + ' must be nonempty text')


def strings(value, where, nonempty=False, unique=True):
    require(isinstance(value, list), 'shape', where + ' must be an array')
    if nonempty:
        require(bool(value), 'empty', where)
    for item in value:
        string(item, where)
    if unique:
        require(len(value) == len(set(value)), 'duplicate', where)


def timestamp(value):
    string(value, 'timestamp')
    try:
        parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError as error:
        raise Invalid('timestamp', value) from error
    require(parsed.tzinfo is not None, 'timestamp', 'Timezone required')
    return parsed


def digest(data):
    return hashlib.sha256(data).hexdigest()


def sha(value, where):
    require(isinstance(value, str) and re.fullmatch(r'[0-9a-f]{64}', value), 'digest', where)


def read_utf8(path):
    data = Path(path).read_bytes()
    try:
        text = data.decode('utf-8')
    except UnicodeError as error:
        raise Invalid('encoding', str(error)) from error
    require('\r' not in text and not text.startswith('\ufeff') and text.endswith('\n'),
            'encoding', 'Use UTF-8 without BOM, LF endings, and a final LF')
    return data, text


def markdown_sections(text, level):
    """Ignore headings inside Markdown fences, including quoted approval text."""
    sections, starts, fence = {}, [], None
    lines = text.splitlines(keepends=True)
    offset = 0
    for line in lines:
        token = re.match(r'^(`{3,}|~{3,})(.*)\n?$', line)
        if fence:
            if token and token[1][0] == fence[0] and len(token[1]) >= fence[1] and not token[2].strip():
                fence = None
        elif token:
            fence = (token[1][0], len(token[1]))
        elif re.match(r'^#{' + str(level) + r'} ', line):
            name = line[level + 1:].strip()
            require(name not in sections, 'duplicate-section', name)
            sections[name] = ''
            starts.append((name, offset, offset + len(line)))
        offset += len(line)
    require(fence is None, 'fence', 'Unclosed Markdown fence')
    for index, (name, start, body) in enumerate(starts):
        end = starts[index + 1][1] if index + 1 < len(starts) else len(text)
        sections[name] = text[body:end]
    return sections


def fenced(body, language):
    body = body.strip('\n')
    match = re.fullmatch(r'(`{3,}|~{3,})' + re.escape(language) + r'\n(.*)\n\1', body, re.S)
    require(match is not None, 'fence', 'Expected one ' + language + ' fence, no extra content')
    return match[2] + '\n'


def json_section(body):
    return strict_json(fenced(body, 'json'))


def scope_payload(body):
    payload = fenced(body, 'yaml')
    lines = payload.splitlines()
    require(lines[0] == 'Scope-Lock-Version: cdf-scope/v1', 'scope-version', 'Expected cdf-scope/v1')
    require(len(lines) == 9, 'scope-format', 'v2 wire profile: eight single-line JSON arrays in canonical order')
    scope = {}
    for key, line in zip(SCOPE_KEYS, lines[1:]):
        require(line.startswith(key + ': '), 'scope-order', key)
        scope[key] = strict_json(line[len(key) + 2:])
        strings(scope[key], key, key in ('in_scope', 'acceptance_criteria'), unique=False)
    require(all(line == line.rstrip() for line in lines), 'scope-format', 'Trailing whitespace')
    return payload, scope


def definition_bytes(data):
    """Exclude only the one top-level digest line in frontmatter, including its LF."""
    require(data.startswith(b'---\n'), 'frontmatter', 'Missing frontmatter')
    end = data.find(b'\n---\n', 4)
    require(end != -1, 'frontmatter', 'Missing closing frontmatter')
    front = data[4:end + 1]
    matches = list(re.finditer(rb'^definition_sha256: [^\n]*\n', front, re.M))
    require(len(matches) == 1, 'missing-digest', 'Exactly one definition_sha256 line is required; never bootstrap a saved task')
    match = matches[0]
    return data[:4 + match.start()] + data[4 + match.end():]


def parse_document(path, check_hashes=True):
    data, text = read_utf8(path)
    # Legacy detection is read-only and deliberately does not attempt migration.
    require(not re.search(r'^task_contract:\s*["\']?cdf-cdtask/v1', text, re.M),
            'legacy-reapproval', 'v1: preserve original; compare approval/history, reapprove and save a separate v2 task')
    require(text.startswith('---\n') and '\n---\n' in text[4:], 'frontmatter', 'Missing frontmatter')
    front, body = text[4:].split('\n---\n', 1)
    meta = {}
    for line in front.splitlines():
        match = re.fullmatch(r'([a-z_][a-z_0-9]*): (.+)', line)
        require(match is not None, 'frontmatter', 'v2 metadata values must be single-line JSON')
        key, value = match.groups()
        require(key not in meta, 'duplicate-key', key)
        meta[key] = strict_json(value)
    fields(meta, META_FIELDS, 'metadata')
    require(meta['task_contract'] == TASK_CONTRACT, 'contract-version', str(meta['task_contract']))
    for key, value in [('handoff_type', 'approved-tasking'), ('status', 'tasking_ready'),
                       ('source', 'cdf'), ('approval_state', 'approved')]:
        require(meta[key] == value, 'metadata', key)
    require(meta['risk_level'] in ['Level S', 'Level M', 'Level L', 'Level XL'], 'risk', 'Invalid risk')
    require(meta['approval_basis'] in ('summary', 'full-plan'), 'approval', 'Invalid basis')
    require(type(meta['phase_scoped']) is bool, 'phase', 'phase_scoped must be boolean')
    require(meta['risk_level'] != 'Level XL' or meta['phase_scoped'], 'phase', 'XL requires approved phase')
    timestamp(meta['created_at'])
    for key in ('workspace', 'source_branch', 'source_commit', 'save_drift_notes'):
        string(meta[key], key)
    require(meta['workspace'] == 'Unavailable' or Path(meta['workspace']).is_absolute(), 'workspace', 'Absolute workspace required')
    require(meta['source_worktree_state'] in ('clean', 'dirty', 'Unavailable'), 'traceability', 'worktree state')
    changes = meta['source_worktree_changes']
    strings(changes, 'source_worktree_changes')
    if changes != ['Unavailable']:
        require(all(re.match(r'^[ MADRCU?!]{2} .+', c) for c in changes), 'traceability', 'Preserve Git XY status')
        require(changes == sorted(changes, key=lambda c: (c[3:], c[:2])), 'traceability', 'Sort status by path then XY')
    require(meta['source_worktree_state'] != 'clean' or changes == [], 'traceability', 'Clean status cannot have changes')
    require(meta['save_drift_preflight'] in ('matched', 'non-material-drift'), 'drift', 'Invalid preflight')
    require((meta['save_drift_notes'] == 'none') == (meta['save_drift_preflight'] == 'matched'), 'drift', 'Preflight notes required')
    sections = markdown_sections(body, 2)
    expected = ['CDF Resume Contract']
    if meta['approval_basis'] == 'summary':
        expected += ['Approval Summary']
    expected += ['Development Plan']
    if meta['phase_scoped']:
        expected += ['Approved Phase Boundary']
    expected += ['Approval Record']
    if 'Partial Approval Result' in sections:
        expected += ['Partial Approval Result']
    expected += ['Dependency Graph', 'Task Definitions', 'Acceptance Mapping', 'Scope Guard',
                 'Future CDF Execution Constraints', 'Compilation Gate Result', 'Save Verification']
    require(list(sections) == expected, 'sections', 'Required sections/order: ' + ', '.join(expected))
    for key, value in sections.items():
        string(value, key)
    resume = json_section(sections['CDF Resume Contract'])
    fields(resume, ['resume_path', 'execution_authorized', 'progress_created_by_save'], 'resume')
    require(resume == {'resume_path': 'CDF only', 'execution_authorized': False, 'progress_created_by_save': False}, 'authorization', 'Save cannot authorize execution')
    if meta['approval_basis'] == 'summary':
        string(fenced(sections['Approval Summary'], 'text'), 'Approval Summary')
    plan = markdown_sections(sections['Development Plan'], 3)
    require(list(plan) == PLAN_HEADINGS, 'plan', 'Development Plan headings/order')
    for key, value in plan.items():
        string(value, key)
    payload, scope = scope_payload(plan['Scope Lock'])
    require(json_section(plan['Acceptance Criteria']) == scope['acceptance_criteria'], 'acceptance-projection', 'Must match canonical entries exactly')
    approval_payload = '## Approval Record\n' + fenced(sections['Approval Record'], 'json')
    require(all(line == line.rstrip() for line in approval_payload.splitlines()), 'approval-format', 'Trailing whitespace')
    approval = json_section(sections['Approval Record'])
    fields(approval, ['user_statement', 'context', 'action', 'type', 'approved_items', 'conditions', 'unapproved_items'], 'approval')
    string(approval['user_statement'], 'user_statement')
    string(approval['context'], 'context')
    require(approval['action'] == 'Save as Task', 'authorization', 'Only Save as Task may persist')
    require(approval['type'] in ('full', 'conditional', 'partial'), 'approval', 'Invalid type')
    require(approval['approved_items'] == scope['in_scope'], 'approval', 'Approved items differ from scope')
    strings(approval['conditions'], 'conditions')
    strings(approval['unapproved_items'], 'unapproved_items')
    require(set(approval['conditions']) <= set(scope['assumptions'] + scope['stop_conditions']), 'approval', 'Conditions must be canonical')
    excluded = scope['out_of_scope'] + scope['non_goals'] + scope['will_not_change']
    require(set(approval['unapproved_items']) <= set(excluded), 'partial', 'Protect unapproved items')
    require((approval['type'] == 'partial') == ('Partial Approval Result' in sections), 'partial', 'Missing/unexpected partial projection')
    if approval['type'] == 'partial':
        projection = json_section(sections['Partial Approval Result'])
        require(projection == {'approved_items': approval['approved_items'], 'unapproved_items': approval['unapproved_items']}, 'partial', 'Projection mismatch')
    if meta['phase_scoped']:
        phase = json_section(sections['Approved Phase Boundary'])
        fields(phase, ['phase', 'scope', 'ends_at', 'explicitly_deferred'], 'phase')
        require(phase['scope'] == scope['in_scope'], 'phase', 'Phase scope mismatch')
        string(phase['phase'], 'phase')
        string(phase['ends_at'], 'ends_at')
        strings(phase['explicitly_deferred'], 'explicitly_deferred')
        require(set(phase['explicitly_deferred']) <= set(excluded), 'phase', 'Protect deferred phases')
    checks = json_section(plan['Verification Strategy'])
    require(isinstance(checks, list) and checks, 'checks', 'Verification Strategy must contain checks')
    check_map = {}
    for check in checks:
        fields(check, ['id', 'kind', 'description'], 'check')
        string(check['id'], 'check id')
        require(check['id'] not in check_map, 'duplicate-id', check['id'])
        require(check['kind'] in ('task', 'product'), 'checks', 'Check kind')
        string(check['description'], 'description')
        check_map[check['id']] = check
    tasks = json_section(sections['Task Definitions'])
    require(isinstance(tasks, list) and tasks, 'tasks', 'No tasks')
    task_map = {}
    ac_ids = ['AC-%03d' % i for i in range(1, len(scope['acceptance_criteria']) + 1)]
    for task in tasks:
        fields(task, TASK_FIELDS, 'task')
        require(isinstance(task['id'], str) and re.fullmatch(r'TASK-\d{3,}', task['id']), 'task-id', 'Invalid ID')
        require(task['id'] not in task_map, 'duplicate-id', task['id'])
        task_map[task['id']] = task
        for key in ('name', 'goal'):
            string(task[key], key)
        for key in ('depends_on', 'scope_mapping', 'write_scope', 'shared_contracts', 'implementation_notes',
                    'contributes_to', 'task_verification', 'must_not_change', 'assumptions_and_stop_conditions'):
            strings(task[key], key, key in ('scope_mapping', 'write_scope', 'contributes_to', 'task_verification'))
        require(set(task['scope_mapping']) <= set(scope['in_scope'] + scope['will_change']), 'scope', 'Noncanonical positive scope')
        require(not set(task['scope_mapping']) & set(excluded), 'scope', 'Excluded positive scope')
        require(set(task['must_not_change']) >= set(excluded), 'scope', 'All exclusions must be protected')
        require(set(task['contributes_to']) <= set(ac_ids), 'acceptance-mapping', 'Unknown AC')
        require(task['contributes_to'] == sorted(task['contributes_to'], key=ac_ids.index), 'acceptance-mapping', 'AC order')
        require(all(c in check_map and check_map[c]['kind'] == 'task' for c in task['task_verification']), 'task-verification', 'Local checks must reference approved task checks')
        require(task['definition_status'] == 'READY', 'tasks', 'Persist only READY definitions')
    graph = json_section(sections['Dependency Graph'])
    require(graph == {t['id']: t['depends_on'] for t in tasks}, 'graph', 'Graph must equal task dependencies')
    visiting, visited = set(), set()
    def visit(task_id):
        require(task_id in task_map, 'dependency', 'Unknown dependency ' + task_id)
        require(task_id not in visiting, 'cycle', 'Dependency cycle at ' + task_id)
        if task_id in visited:
            return
        visiting.add(task_id)
        for dep in graph[task_id]:
            visit(dep)
        visiting.remove(task_id)
        visited.add(task_id)
    for task_id in task_map:
        visit(task_id)
    mapping = json_section(sections['Acceptance Mapping'])
    fields(mapping, ac_ids, 'Acceptance Mapping')
    require(list(mapping) == ac_ids, 'acceptance-mapping', 'Mapping must preserve canonical AC order')
    for ac_id in ac_ids:
        strings(mapping[ac_id], ac_id, nonempty=True)
        require(all(c in check_map and check_map[c]['kind'] == 'product' for c in mapping[ac_id]), 'acceptance-mapping', 'Product checks required')
        require(any(ac_id in t['contributes_to'] for t in tasks), 'acceptance-coverage', ac_id)
    used = {c for t in tasks for c in t['task_verification']} | {c for ids in mapping.values() for c in ids}
    require(used == set(check_map), 'checks', 'Every approved check must have a verification path')
    guard = json_section(sections['Scope Guard'])
    fields(guard, ['result', 'evidence'], 'Scope Guard')
    require(guard['result'] == 'checked', 'scope-guard', 'Scope Guard result')
    string(guard['evidence'], 'Scope Guard evidence')
    require(json_section(sections['Compilation Gate Result']) == {'status': 'READY', 'task_count': len(tasks)}, 'compilation', 'Invalid compilation result')
    save = json_section(sections['Save Verification'])
    fields(save, ['status', 'verified_at'], 'Save Verification')
    require(save['status'] == 'verified', 'save', 'Save read-back not verified')
    timestamp(save['verified_at'])
    hashes = {'scope_lock_sha256': digest(payload.encode()),
              'approval_record_sha256': digest(approval_payload.encode()),
              'definition_sha256': digest(definition_bytes(data))}
    if check_hashes:
        for key, value in hashes.items():
            sha(meta[key], key)
            require(meta[key] == value, 'integrity-mismatch', key + ' does not match saved baseline; do not repair')
    return {'meta': meta, 'scope': scope, 'checks': check_map, 'tasks': task_map,
            'mapping': mapping, 'hashes': hashes, 'document_sha256': digest(data)}


def evidence_index(items):
    require(isinstance(items, list), 'evidence', 'Evidence must be an array')
    result = {}
    for item in items:
        fields(item, ['id', 'kind', 'source', 'result', 'snapshot', 'check_id', 'valid'], 'evidence')
        for key in ('id', 'kind', 'source', 'result', 'snapshot'):
            string(item[key], key)
        sha(item['snapshot'], 'evidence snapshot')
        require(item['check_id'] is None or isinstance(item['check_id'], str), 'evidence', 'check_id')
        require(type(item['valid']) is bool, 'evidence', 'valid must be boolean')
        require(item['id'] not in result, 'duplicate-id', item['id'])
        result[item['id']] = item
    return result


def refs(ids, evidence, current=False, snapshot=None, nonempty=True):
    strings(ids, 'evidence references', nonempty)
    require(set(ids) <= evidence.keys(), 'evidence-ref', 'Unresolved evidence ID')
    if current:
        require(all(evidence[i]['valid'] for i in ids), 'stale-evidence', 'Invalidated evidence')
    if snapshot:
        require(all(evidence[i]['snapshot'] == snapshot for i in ids), 'stale-evidence', 'Snapshot mismatch')


def successful(ids, evidence, snapshot=None):
    refs(ids, evidence, True, snapshot)
    require(all(evidence[i]['result'] == 'PASS' for i in ids), 'evidence-result', 'Successful evidence required')


def validate_gate(gate, doc, snapshot):
    fields(gate, GATE_FIELDS, 'completion_gate')
    require(gate['status'] in ('PASS', 'FAIL', 'INSUFFICIENT_EVIDENCE'), 'gate', 'Unknown gate decision')
    timestamp(gate['evaluated_at'])
    sha(gate['source_snapshot'], 'gate snapshot')
    evidence = evidence_index(gate['evidence'])
    passing = gate['status'] == 'PASS'
    if passing:
        require(gate['source_snapshot'] == snapshot, 'stale-gate', 'Gate snapshot is stale')
    for name in GATE_FIELDS[1:8]:
        require(isinstance(gate[name], list), 'gate', name + ' must be an array')
    criteria = gate['acceptance_criteria']
    require([c.get('criterion') for c in criteria if isinstance(c, dict)] == doc['scope']['acceptance_criteria'], 'completion-coverage', 'Report every canonical AC in order')
    for ac_id, row in zip(doc['mapping'], criteria):
        fields(row, ['criterion', 'result', 'evidence'], 'criterion result')
        require(row['result'] in ('PASS', 'FAIL', 'UNVERIFIED'), 'gate', 'Criterion result')
        refs(row['evidence'], evidence, nonempty=row['result'] == 'PASS')
        if passing:
            require(row['result'] == 'PASS', 'gate', 'Nonpassing criterion')
            successful(row['evidence'], evidence, snapshot)
            require(set(doc['mapping'][ac_id]) <= {evidence[i]['check_id'] for i in row['evidence']}, 'completion-checks', 'Missing planned product check')
    established_failure = any(row['result'] == 'FAIL' for row in criteria) or bool(gate['out_of_scope_changes'])
    for row in gate['validation_results']:
        fields(row, ['check', 'required', 'result', 'command', 'working_directory', 'exit_code', 'reason', 'evidence'], 'validation result')
        require(type(row['required']) is bool, 'gate', 'required must be boolean')
        require(row['result'] in ('PASS', 'FAIL', 'NOT_RUN', 'UNKNOWN', 'NOT_APPLICABLE'), 'gate', 'Validation result')
        for key in ('check', 'command', 'working_directory', 'reason'):
            string(row[key], key)
        require(row['exit_code'] is None or type(row['exit_code']) is int, 'gate', 'Exit code')
        refs(row['evidence'], evidence, nonempty=row['result'] in ('PASS', 'NOT_APPLICABLE'))
        established_failure = established_failure or row['result'] == 'FAIL' or (row['required'] and row['exit_code'] not in (None, 0))
        if row['result'] == 'PASS':
            require(row['exit_code'] in (None, 0), 'gate', 'Nonzero exit contradicts PASS')
        if passing:
            require(row['result'] != 'FAIL' and (not row['required'] or row['result'] == 'PASS'), 'gate', 'Failed or unrun required check')
            if row['result'] == 'PASS':
                successful(row['evidence'], evidence, snapshot)
                if row['check'] in doc['checks']:
                    require(row['check'] in {evidence[i]['check_id'] for i in row['evidence']}, 'completion-checks', 'Validation evidence must identify its check')
    if established_failure:
        require(gate['status'] == 'FAIL', 'gate', 'Established failure takes precedence over missing evidence')
    if passing:
        require({'tests', 'lint', 'typecheck', 'build'} <= {r['check'] for r in gate['validation_results']}, 'gate', 'Account for validation categories')
        required_checks = set(doc['checks'])
        passed_checks = {r['check'] for r in gate['validation_results'] if r['result'] == 'PASS' and r['required']}
        require(required_checks <= passed_checks, 'completion-checks', 'All approved checks need successful validation rows')
        require(not gate['out_of_scope_changes'] and not gate['unverified_items'], 'gate', 'Scope violation or evidence gap prevents PASS')
        for kind in ('agent_activity', 'diff_review', 'scope_compliance'):
            ids = [i for i, e in evidence.items() if e['kind'] == kind and e['valid'] and e['snapshot'] == snapshot and e['result'] == 'PASS']
            require(ids, 'gate-evidence', 'Missing ' + kind)
    shapes = {'changed_files': ['path', 'change', 'evidence'],
              'out_of_scope_changes': ['path', 'change', 'reason', 'evidence'],
              'known_issues': ['issue', 'impact', 'evidence'],
              'unverified_items': ['item', 'reason', 'impact', 'evidence']}
    for name, keys in shapes.items():
        for row in gate[name]:
            fields(row, keys, name)
            for key in keys[:-1]:
                string(row[key], key)
            refs(row['evidence'], evidence, current=passing, snapshot=snapshot if passing else None,
                 nonempty=name in ('changed_files', 'out_of_scope_changes'))
    return evidence


def descendants(tasks, root):
    found = set()
    todo = [root]
    while todo:
        parent = todo.pop()
        for task_id, task in tasks.items():
            if parent in task['depends_on'] and task_id not in found:
                found.add(task_id)
                todo.append(task_id)
    return found


def validate_progress(progress, doc, path, previous=None, snapshot=None):
    fields(progress, ['progress_contract', 'task_path', 'task_contract', 'task_document_sha256',
                      'definition_sha256', 'scope_lock_sha256', 'approval_record_sha256',
                      'overall_state', 'created_at', 'updated_at', 'completed_at', 'source_snapshot',
                      'authorizations', 'events', 'tasks', 'evidence', 'completion_gate', 'final_review',
                      'completion_history'], 'progress')
    require(progress['progress_contract'] == PROGRESS_CONTRACT and progress['task_contract'] == TASK_CONTRACT, 'progress-version', 'Legacy or mixed progress contract')
    require(progress['task_path'] == str(Path(path).resolve()), 'binding', 'Task path mismatch')
    for key in ('definition_sha256', 'scope_lock_sha256', 'approval_record_sha256'):
        require(progress[key] == doc['hashes'][key], 'binding', key)
    require(progress['task_document_sha256'] == doc['document_sha256'], 'binding', 'Document hash mismatch')
    created, updated = timestamp(progress['created_at']), timestamp(progress['updated_at'])
    require(created <= updated, 'timestamp', 'updated_at precedes created_at')
    sha(progress['source_snapshot'], 'source_snapshot')
    snapshot = snapshot or progress['source_snapshot']
    require(progress['source_snapshot'] == snapshot, 'snapshot', 'Current snapshot differs')
    require(progress['overall_state'] in ('not_started', 'in_progress', 'blocked', 'completed'), 'state', 'overall_state')
    authorizations = progress['authorizations']
    require(isinstance(authorizations, list) and authorizations, 'authorization', 'Runtime requires explicit resume authorization')
    auth_map = {}
    for auth in authorizations:
        fields(auth, ['id', 'user_request', 'context', 'task_path', 'definition_sha256', 'action'], 'authorization')
        for key in ('id', 'user_request', 'context'):
            string(auth[key], key)
        require(auth['id'] not in auth_map, 'duplicate-id', 'authorization')
        require(auth['action'] == 'Execute Saved Approved Scope', 'authorization', 'Inspect/save is not execute')
        require(auth['task_path'] == progress['task_path'] and auth['definition_sha256'] == progress['definition_sha256'], 'authorization', 'Authorization binding')
        auth_map[auth['id']] = auth
    evidence = evidence_index(progress['evidence'])
    states = {task_id: 'pending' for task_id in doc['tasks']}
    current_refs = {task_id: [] for task_id in doc['tasks']}
    last_time = created
    invalidated = set()
    require(isinstance(progress['events'], list), 'events', 'events must be an array')
    for index, event in enumerate(progress['events']):
        fields(event, ['seq', 'task_id', 'from', 'to', 'at', 'authorization', 'reason', 'evidence',
                       'affected_tasks', 'scope_evidence', 'new_decisions'], 'event')
        require(type(event['seq']) is int and event['seq'] == index + 1, 'event-order', 'Sequential event numbers required')
        task_id = event['task_id']
        require(isinstance(task_id, str) and task_id in states, 'task-id', 'Unknown event task')
        require(event['authorization'] in auth_map, 'authorization', 'Unknown authorization')
        event_time = timestamp(event['at'])
        require(last_time <= event_time <= updated, 'event-order', 'Event time out of order')
        last_time = event_time
        require(event['from'] == states[task_id] and event['to'] in TRANSITIONS[states[task_id]], 'transition', 'Illegal transition for ' + task_id)
        string(event['reason'], 'event reason')
        require(type(event['new_decisions']) is bool and not event['new_decisions'], 'scope', 'New decisions require replan')
        refs(event['evidence'], evidence, nonempty=event['to'] == 'verified')
        strings(event['affected_tasks'], 'affected_tasks')
        refs(event['scope_evidence'], evidence, nonempty=event['from'] == 'verified')
        if event['to'] == 'in_progress':
            require(all(states[d] == 'verified' for d in doc['tasks'][task_id]['depends_on']), 'dependency-state', 'Dependencies not verified')
        if event['from'] == 'verified':
            affected = descendants(doc['tasks'], task_id)
            require(set(event['affected_tasks']) == affected, 'reopen', 'Account for every downstream task')
            for affected_id in affected | {task_id}:
                invalidated.update(current_refs[affected_id])
                current_refs[affected_id] = []
                if affected_id != task_id and states[affected_id] != 'pending':
                    states[affected_id] = 'blocked'
        else:
            require(not event['affected_tasks'], 'reopen', 'affected_tasks only for reopen')
        if event['to'] == 'verified':
            require(all(evidence[i]['result'] == 'PASS' for i in event['evidence']), 'evidence-result', 'Verification needs observed success')
            require(not set(event['evidence']) & invalidated, 'stale-evidence', 'Cannot reuse invalidated evidence')
            checks = {evidence[i]['check_id'] for i in event['evidence']}
            require(set(doc['tasks'][task_id]['task_verification']) <= checks, 'task-verification', 'Missing local verification')
            current_refs[task_id] = event['evidence']
        states[task_id] = event['to']
    require(all(not evidence[i]['valid'] for i in invalidated), 'reopen', 'Old evidence must be invalidated, not removed')
    rows = progress['tasks']
    require(isinstance(rows, list), 'tasks', 'Progress tasks must be array')
    require([r.get('id') for r in rows if isinstance(r, dict)] == list(doc['tasks']), 'tasks', 'Progress IDs/order mismatch')
    for row in rows:
        fields(row, ['id', 'state', 'verification_evidence'], 'progress task')
        task_id = row['id']
        require(row['state'] == states[task_id] and row['verification_evidence'] == current_refs[task_id], 'state', 'State must equal replayed journal')
        if row['state'] == 'verified':
            successful(row['verification_evidence'], evidence)
    gate, review = progress['completion_gate'], progress['final_review']
    if gate is not None:
        validate_gate(gate, doc, snapshot)
        require(timestamp(gate['evaluated_at']) <= updated, 'timestamp', 'Gate after updated_at')
        if gate['status'] == 'PASS':
            require(all(s == 'verified' for s in states.values()) and last_time <= timestamp(gate['evaluated_at']), 'stale-gate', 'Move stale gate/review to history after task changes')
    if review is not None:
        fields(review, REVIEW_FIELDS, 'final_review')
        require(gate is not None and gate['status'] == 'PASS', 'review', 'Review follows gate PASS')
        require(timestamp(gate['evaluated_at']) <= timestamp(review['reviewed_at']) <= updated, 'review', 'Review must follow gate')
        require(review['result'] in ('PASS', 'FAIL', 'PENDING'), 'review', 'Unknown result')
        strings(review['outstanding_findings'], 'outstanding_findings')
        require(type(review['required_approval']) is bool, 'review', 'required_approval')
        refs(review['approval_evidence'], evidence, nonempty=review['required_approval'] and review['result'] == 'PASS')
        refs(review['evidence'], evidence, nonempty=review['result'] != 'PENDING')
        if review['result'] == 'PASS':
            require(review['source_snapshot'] == snapshot and not review['outstanding_findings'], 'review', 'Stale or unresolved final review')
            successful(review['evidence'], evidence, snapshot)
            require(all(evidence[i]['kind'] == 'final_review' for i in review['evidence']), 'review', 'Reference actual final review evidence')
            if review['required_approval']:
                successful(review['approval_evidence'], evidence, snapshot)
                require(all(evidence[i]['kind'] == 'human_approval' for i in review['approval_evidence']), 'review', 'Approval must reference human approval evidence')
    require(isinstance(progress['completion_history'], list), 'history', 'completion_history must be an array')
    for attempt in progress['completion_history']:
        fields(attempt, ['completion_gate', 'final_review', 'invalidated_reason'], 'completion history')
        string(attempt['invalidated_reason'], 'invalidated_reason')
        require(isinstance(attempt['completion_gate'], dict), 'history', 'Preserve historical gate')
    if progress['overall_state'] == 'not_started':
        require(not progress['events'], 'state', 'not_started with execution events')
    if progress['overall_state'] == 'completed':
        require(all(s == 'verified' for s in states.values()), 'completion', 'Tasks not locally verified')
        require(gate is not None and gate['status'] == 'PASS', 'completion', 'Completion Gate missing or nonpassing')
        require(review is not None and review['result'] == 'PASS', 'completion', 'Final review required')
        require(last_time <= timestamp(gate['evaluated_at']), 'completion', 'Gate predates task changes')
        require(timestamp(review['reviewed_at']) <= timestamp(progress['completed_at']) <= updated, 'completion', 'Invalid completed_at')
    else:
        require(progress['completed_at'] is None, 'completion', 'Incomplete run cannot have completed_at')
    if previous is not None:
        # Validate the previous document on its own snapshot before comparing append-only history.
        validate_progress(previous, doc, path)
        for key in ('created_at', 'task_path', 'task_contract', 'task_document_sha256', 'definition_sha256'):
            require(progress[key] == previous[key], 'history', 'Runtime identity rewritten: ' + key)
        require(timestamp(progress['updated_at']) >= timestamp(previous['updated_at']), 'history', 'updated_at moved backwards')
        for key in ('authorizations', 'events', 'completion_history'):
            require(progress[key][:len(previous[key])] == previous[key], 'history', 'History rewritten: ' + key)
        for old in previous['evidence']:
            require(old['id'] in evidence, 'history', 'Evidence deleted')
            new = evidence[old['id']]
            require({k: v for k, v in old.items() if k != 'valid'} == {k: v for k, v in new.items() if k != 'valid'}, 'history', 'Evidence rewritten')
            require(old['valid'] or not new['valid'], 'history', 'Evidence cannot be revalidated by toggling valid')
        if previous['completion_gate'] is not None and (previous['completion_gate'] != gate or previous['final_review'] != review):
            require(any(a['completion_gate'] == previous['completion_gate'] and a['final_review'] == previous['final_review'] for a in progress['completion_history']), 'history', 'Preserve prior completion/review attempt')
    return states


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('task', nargs='?')
    parser.add_argument('--progress', help='Read JSON-compatible YAML progress sidecar')
    parser.add_argument('--previous-progress', help='Compare an earlier journal snapshot; never overwrite it')
    parser.add_argument('--snapshot', help='Independently computed current source snapshot SHA-256')
    parser.add_argument('--draft-hashes', action='store_true', help='Print hashes for an UNSAVED approved draft only; never modifies files or validates saved integrity')
    parser.add_argument('--describe', action='store_true', help='Print authoritative mechanical field names and transitions')
    args = parser.parse_args(argv)
    try:
        if args.describe:
            print(json.dumps({'task_contract': TASK_CONTRACT, 'progress_contract': PROGRESS_CONTRACT,
                              'scope_fields': SCOPE_KEYS, 'plan_headings': PLAN_HEADINGS,
                              'metadata_fields': META_FIELDS, 'task_fields': TASK_FIELDS,
                              'gate_fields': GATE_FIELDS, 'review_fields': REVIEW_FIELDS,
                              'transitions': TRANSITIONS}, indent=2))
            return 0
        require(args.task is not None, 'usage', 'task is required')
        require(not args.draft_hashes or not (args.progress or args.previous_progress), 'usage', 'Draft hashes cannot validate runtime')
        require(not args.previous_progress or args.progress, 'usage', '--previous-progress requires --progress')
        doc = parse_document(args.task, check_hashes=not args.draft_hashes)
        if args.progress:
            _, progress_text = read_utf8(args.progress)
            previous = None
            if args.previous_progress:
                _, previous_text = read_utf8(args.previous_progress)
                previous = strict_json(previous_text)
            validate_progress(strict_json(progress_text), doc, args.task, previous, args.snapshot)
        print(json.dumps({'mechanical_status': 'DRAFT_HASHES_ONLY' if args.draft_hashes else 'VALID',
                          'hashes': doc['hashes'], 'review_required': SEMANTIC_REVIEW,
                          'execution_authorized': False}, ensure_ascii=False, indent=2))
        return 0
    except (Invalid, OSError, ValueError, TypeError, KeyError, AttributeError, IndexError, RecursionError) as error:
        code = error.code if isinstance(error, Invalid) else 'malformed-or-io'
        print(json.dumps({'mechanical_status': 'INVALID', 'errors': [{'code': code, 'message': str(error)}],
                          'execution_authorized': False}, ensure_ascii=False))
        return 1


if __name__ == '__main__':
    sys.exit(main())
