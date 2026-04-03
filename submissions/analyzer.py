import re
import ast

def analyze_code(code, language):
    """
    Real code analysis engine - checks actual code quality
    """
    bugs = []
    performance_issues = []
    best_practices = []
    security_issues = []

    lines = code.split('\n')
    total_lines = len(lines)

    # === SCORING BASE ===
    readability = 100.0
    performance = 100.0
    security = 100.0
    best_prac = 100.0

    if language == 'python':
        # --- Bug Detection ---
        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            # Bare except
            if re.search(r'\bexcept\s*:', stripped):
                bugs.append({
                    'line': i, 'severity': 'medium',
                    'type': 'Bare Except',
                    'message': f'Line {i}: Bare `except:` catches everything including KeyboardInterrupt.',
                    'fix': 'Use `except Exception as e:` or specify the exception type.'
                })
                readability -= 5

            # == None comparison
            if re.search(r'==\s*None|None\s*==', stripped):
                bugs.append({
                    'line': i, 'severity': 'low',
                    'type': 'None Comparison',
                    'message': f'Line {i}: Avoid `== None`, use `is None` instead.',
                    'fix': 'Replace `== None` with `is None`'
                })
                best_prac -= 3

            # Mutable default argument
            if re.search(r'def\s+\w+\s*\(.*=\s*[\[\{]', stripped):
                bugs.append({
                    'line': i, 'severity': 'high',
                    'type': 'Mutable Default Argument',
                    'message': f'Line {i}: Using mutable default argument (list/dict). This is a common Python bug.',
                    'fix': 'Use `None` as default and initialize inside function.'
                })
                security -= 8

            # Print statements (not ideal in production)
            if re.match(r'\s*print\s*\(', line) and 'debug' not in line.lower():
                best_practices.append({
                    'line': i,
                    'type': 'Debug Print',
                    'message': f'Line {i}: `print()` found. Use logging module for production code.',
                    'fix': 'Replace with `import logging` and `logging.debug()`'
                })
                best_prac -= 2

        # --- Performance ---
        if 'for' in code and 'append' in code:
            performance_issues.append({
                'type': 'List Building',
                'message': 'Using loop + append to build list. List comprehension is faster.',
                'fix': 'Try: `result = [x for x in items]` instead of loop+append',
                'improvement': '30-50% faster'
            })
            performance -= 10

        if code.count('for') > 2 and code.count('for') > code.count('enumerate'):
            performance_issues.append({
                'type': 'Missing enumerate()',
                'message': 'Using range(len()) pattern. enumerate() is more Pythonic and faster.',
                'fix': 'Use `for i, val in enumerate(items):` instead of `for i in range(len(items)):`',
                'improvement': '10-20% cleaner'
            })
            performance -= 5

        # --- Security ---
        if 'eval(' in code or 'exec(' in code:
            security_issues.append({
                'severity': 'critical',
                'type': 'Code Injection Risk',
                'message': '`eval()` or `exec()` found! This allows arbitrary code execution.',
                'fix': 'Never use eval/exec with user input. Use ast.literal_eval() for safe evaluation.'
            })
            security -= 25
            bugs.append({
                'line': 0, 'severity': 'critical',
                'type': 'Security: Code Injection',
                'message': 'CRITICAL: eval()/exec() detected. Major security vulnerability.',
                'fix': 'Remove eval/exec or use ast.literal_eval() for safe parsing.'
            })

        if 'input(' in code and ('eval' in code or 'exec' in code):
            security -= 20

        if 'password' in code.lower() and ('=' in code) and ('"' in code or "'" in code):
            if re.search(r'password\s*=\s*["\']', code, re.IGNORECASE):
                security_issues.append({
                    'severity': 'high',
                    'type': 'Hardcoded Password',
                    'message': 'Hardcoded password detected in source code!',
                    'fix': 'Use environment variables: `os.environ.get("PASSWORD")`'
                })
                security -= 20

        # --- Readability ---
        long_lines = [i+1 for i, l in enumerate(lines) if len(l) > 79]
        if long_lines:
            best_practices.append({
                'line': long_lines[0],
                'type': 'Line Length',
                'message': f'{len(long_lines)} lines exceed PEP 8 limit of 79 chars (lines: {long_lines[:3]}...)',
                'fix': 'Break long lines using parentheses or backslash continuation.'
            })
            readability -= min(10, len(long_lines) * 2)

        # Check function docstrings
        func_count = len(re.findall(r'def\s+\w+', code))
        doc_count = len(re.findall(r'"""', code)) // 2
        if func_count > 0 and doc_count < func_count:
            best_practices.append({
                'line': 0,
                'type': 'Missing Docstrings',
                'message': f'{func_count - doc_count} functions missing docstrings.',
                'fix': 'Add docstrings: `def func(): """Description."""`'
            })
            readability -= min(15, (func_count - doc_count) * 3)

        # Variable naming
        bad_vars = re.findall(r'\b([a-z])\s*=\s*(?!lambda)', code)
        if len(bad_vars) > 2:
            best_practices.append({
                'line': 0,
                'type': 'Poor Variable Names',
                'message': f'Found {len(bad_vars)} single-letter variables. Use descriptive names.',
                'fix': 'Use descriptive names: `count` instead of `c`, `user_list` instead of `l`'
            })
            readability -= min(10, len(bad_vars) * 2)

    elif language == 'javascript':
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if 'var ' in stripped:
                bugs.append({
                    'line': i, 'severity': 'medium',
                    'type': 'var Usage',
                    'message': f'Line {i}: `var` is function-scoped and hoisted. Use `let` or `const`.',
                    'fix': 'Replace `var` with `const` (if not reassigned) or `let`'
                })
                best_prac -= 5
            if '==' in stripped and '===' not in stripped and '!==' not in stripped:
                bugs.append({
                    'line': i, 'severity': 'low',
                    'type': 'Loose Equality',
                    'message': f'Line {i}: `==` does type coercion. Use `===` for strict comparison.',
                    'fix': 'Replace `==` with `===` and `!=` with `!==`'
                })
                best_prac -= 3
            if 'console.log' in stripped:
                best_practices.append({
                    'line': i, 'type': 'Debug Log',
                    'message': f'Line {i}: console.log() found. Remove before production.',
                    'fix': 'Remove console.log() or use a logging library'
                })
                best_prac -= 2

    # === COMPUTE FINAL SCORES ===
    readability = max(20, min(100, readability))
    performance = max(20, min(100, performance))
    security = max(20, min(100, security))
    best_prac = max(20, min(100, best_prac))

    # Bonus for good practices
    if total_lines > 10 and len(bugs) == 0:
        readability = min(100, readability + 5)
    if '"""' in code or "'''" in code:
        readability = min(100, readability + 5)

    overall = round((readability * 0.3 + performance * 0.3 + security * 0.2 + best_prac * 0.2), 1)

    # Points calculation
    points = int(overall / 10) * 10
    if overall >= 90:
        points += 50
    elif overall >= 75:
        points += 25
    elif overall >= 60:
        points += 10

    return {
        'overall_score': overall,
        'readability_score': round(readability, 1),
        'performance_score': round(performance, 1),
        'security_score': round(security, 1),
        'best_practices_score': round(best_prac, 1),
        'bugs': bugs,
        'performance_issues': performance_issues,
        'best_practices': best_practices,
        'security_issues': security_issues,
        'bugs_found': len(bugs),
        'points_earned': points,
        'lines_analyzed': total_lines,
        'grade': get_grade(overall),
        'summary': get_summary(overall, len(bugs)),
    }

def get_grade(score):
    if score >= 90: return {'letter': 'A+', 'color': '#22c55e', 'emoji': '🏆'}
    if score >= 80: return {'letter': 'A', 'color': '#4ade80', 'emoji': '⭐'}
    if score >= 70: return {'letter': 'B', 'color': '#facc15', 'emoji': '👍'}
    if score >= 60: return {'letter': 'C', 'color': '#fb923c', 'emoji': '📝'}
    return {'letter': 'D', 'color': '#ef4444', 'emoji': '⚠️'}

def get_summary(score, bugs):
    if score >= 90 and bugs == 0:
        return "Excellent code! Clean, secure, and well-structured. Production ready! 🚀"
    if score >= 80:
        return "Great code quality! Minor improvements possible. Almost production-ready. ⭐"
    if score >= 70:
        return "Good code with some issues. Fix the highlighted problems to improve quality. 👍"
    if score >= 60:
        return "Decent code but needs improvement. Address bugs and security issues. 📝"
    return "Code needs significant work. Multiple issues detected. Review carefully. ⚠️"
