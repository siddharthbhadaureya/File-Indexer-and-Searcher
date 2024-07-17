from pathlib import Path

root = Path('E:/Computer Science/Python')
exclude = ('__pycache__', 'logs', 'Lib', 'lib')

def foo(f):
    try:
        for i in f.iterdir():
            if i.is_dir():
                if i not in exclude:
                    yield from foo(i)
            if str(i).endswith('.py'):
                yield i
    except OSError:
        pass
        
        
