"""Deterministic product checks, not approval or acceptance inference."""
import re
import unittest
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills' / 'devloop'
TEMPLATES = SKILL / 'assets' / 'templates'


def markdown_targets(text):
    for match in re.finditer(r'(?<!!)\[[^\]\n]*\]\((?:<([^>]+)>|([^\s)]+))(?:\s+"[^"]*")?\)', text):
        yield match.group(1) or match.group(2)


class SkillStructure(unittest.TestCase):
    def test_entry_and_routes(self):
        entry = (SKILL / 'SKILL.md').read_text()
        self.assertTrue(entry.startswith('---\nname: devloop\n'))
        self.assertLess(len(entry.splitlines()), 500)
        self.assertIn('protocol-version: "2"', entry)
        routes = re.findall(r'\$_S/((?:references|assets)/[\w./-]+)', entry)
        self.assertGreaterEqual(len(routes), 5)
        for route in routes:
            self.assertTrue((SKILL / route).exists(), route)
        phases = set(re.findall(r'references/(phase-[a-z-]+\.md)', entry))
        self.assertEqual(len(phases), 6)
        for phase in phases:
            self.assertTrue((SKILL / 'references' / phase).is_file(), phase)

    def test_product_local_links(self):
        for path in SKILL.rglob('*.md'):
            for target in markdown_targets(path.read_text()):
                if target.startswith(('https:', 'http:', 'mailto:', '#')):
                    continue
                dest = unquote(target.split('#', 1)[0])
                resolved = (path.parent / dest).resolve()
                self.assertTrue(resolved.is_relative_to(SKILL.resolve()), (path, target))
                self.assertTrue(resolved.exists(), (path, target))

    def test_no_developer_context_dependency(self):
        for path in SKILL.rglob('*.md'):
            text = path.read_text()
            self.assertNotIn('docs/redesign', text, path)
            self.assertNotIn('devloop-redesign-audit', text, path)

    def test_template_frontmatter_defaults(self):
        allowed = {
            'vision': {'draft'}, 'spec': {'draft'}, 'ac': {'draft'},
            'interface': {'draft'}, 'adr': {'draft'},
            'delivery': {'planned'}, 'plan': {'pending'}, 'report': {'draft'},
        }
        seen = set()
        for path in TEMPLATES.rglob('*.md'):
            text = path.read_text()
            if not text.startswith('---\n'):
                continue
            header = text.split('---', 2)[1]
            values = dict(re.findall(r'^([a-z][\w-]*):\s*(.*)$', header, re.M))
            self.assertTrue({'title', 'description', 'type', 'status'} <= values.keys(), path)
            kind = values['type']
            self.assertIn(kind, allowed, path)
            self.assertIn(values['status'], allowed[kind], path)
            self.assertNotIn('created', values, path)
            seen.add(kind)
        self.assertEqual(seen, set(allowed))

    def test_resident_rules_and_delivery_navigation(self):
        agents = (TEMPLATES / 'AGENTS.md').read_text()
        resident = (TEMPLATES / 'docs' / 'devloop.md').read_text()
        for concept in ('授权', '变更', '接管', '评审'):
            self.assertIn(concept, agents + resident)
        self.assertIn('devloop.md', agents)
        review_resident = (TEMPLATES / 'docs/review.md').read_text()
        self.assertIn('review.md', resident)
        self.assertIn('独立', review_resident)
        self.assertIn('资源不可用', review_resident)
        self.assertIn('deliveries', (TEMPLATES / 'docs' / 'README.md').read_text())

    def test_engineering_choices_have_resident_activation(self):
        entry = (SKILL / 'SKILL.md').read_text()
        work = (SKILL / 'references/work-and-delivery.md').read_text()
        resident = (TEMPLATES / 'docs/devloop.md').read_text()
        agents = (TEMPLATES / 'AGENTS.md').read_text()
        contributing = (TEMPLATES / 'CONTRIBUTING.md').read_text()
        for text in (entry, work, resident, agents, contributing):
            self.assertIn('短期工作分支', text)
            self.assertIn('未提交', text)
        for concept in ('最小实验', '失败用例', '自动检查', 'diff', '检查点'):
            self.assertIn(concept, resident)
        self.assertIn('不逐项', resident)
        self.assertNotIn('可从 Gitflow', contributing)
        self.assertIn('默认先捕获最小失败用例', contributing)

    def test_review_and_risk_have_runtime_and_resident_routes(self):
        entry = (SKILL / 'SKILL.md').read_text()
        protocol = (SKILL / 'references/review-and-risk.md').read_text()
        agents = (TEMPLATES / 'AGENTS.md').read_text()
        resident = (TEMPLATES / 'docs/review.md').read_text()
        self.assertIn('$_S/references/review-and-risk.md', entry)
        self.assertTrue((TEMPLATES / 'REVIEW.md').is_file())
        for text in (protocol, resident):
            for concept in ('第三轮', '独立核验', '归因', 'low', 'medium', 'high'):
                self.assertIn(concept, text)
        self.assertIn('REVIEW.md', agents)
        self.assertIn('docs/review.md', agents)
        for concept in ('三轮', '核验', '风险'):
            self.assertIn(concept, agents)
        report = (TEMPLATES / 'docs/plans/0001-template/01-report-example.md').read_text()
        for concept in ('finding', '基线', '关闭', '升级'):
            self.assertIn(concept, report)

    def test_removed_absolute_rules_do_not_return(self):
        forbidden = (
            '文档变更和代码变更永远分开 commit',
            '丢弃 branch/worktree，任务重置为 pending',
            '每条 AC 必须覆盖四个场景',
            'Spec 已 active → 在现有文档上追加，不重写',
            '修改必须 Leader 参与',
        )
        for path in SKILL.rglob('*.md'):
            for phrase in forbidden:
                self.assertNotIn(phrase, path.read_text(), path)


if __name__ == '__main__':
    unittest.main()
