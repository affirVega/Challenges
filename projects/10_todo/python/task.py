from datetime import date
import re

def to_date(date_str: str) -> date | None:
    if not re.match('\d{4}-\d{2}-\d{2}', date_str):
        return None
    try:
        return date.fromisoformat(date_str)
    except ValueError:
        return None

def to_priority(p_str: str) -> str | None:
    if m := re.match('\(([A-Z])\)$', p_str):
        return m.group(1)
    return None

class Task:
    completed:       bool     
    priority:        str      
    completion_date: date     
    creation_date:   date     
    description:     str      
    project_tags:    list[str]
    context_tags:    list[str]
    key_values:      dict     

    def __init__(self,
            completed:       bool      = False,
            priority:        str       = None,
            completion_date: date      = None,
            creation_date:   date      = None,
            description:     str       = '',
            project_tags:    list[str] = None,
            context_tags:    list[str] = None,
            key_values:      dict      = None):
        '''
        Priority must be one A-Z character. Example: 'A'
        '''

        self.completed = completed
        self.priority = priority
        self.completion_date = completion_date
        self.creation_date = creation_date
        self.description = description
        self.project_tags = project_tags if project_tags else list()
        self.context_tags = context_tags if context_tags else list()
        self.key_values = key_values if key_values else dict()

    def __repr__(self) -> str:
        return f'''Task({self.completed=}, {self.priority=}, \
{self.completion_date=}, {self.creation_date=}, {self.description=}, \
{self.project_tags=}, {self.context_tags=}, {self.key_values=})'''.replace('self.', '')

    def __str__(self) -> str:
        s = ''
        if self.completed:
            s += 'x '
        if self.completion_date:
            s += self.completion_date.isoformat() + ' '
        if self.priority:
            s += '(' + self.priority + ') '
        if self.creation_date:
            s += self.creation_date.isoformat() + ' '
        if self.description:
            s += self.description
        return s
        
    @staticmethod
    def parse(line: str) -> 'Task':
        task = Task()

        # x (A) 2020-05-20 2020-05-20 description +projectTag @contextTag key:value
        tokens = line.split(' ')
        
        state = 0
        for token in tokens:
            if state != 4:
                if state == 0 and token == 'x':
                    task.completed = True
                    state = 1
                elif d := to_date(token):
                    if state == 1:
                        task.completion_date = d
                        state = 3
                    else:
                        task.creation_date = d
                        state = 'e'
                        continue
                elif state != 2:
                    if p := to_priority(token):
                        task.priority = p
                        state = 2
                    else:
                        state = 4
                else:
                    state = 4

            if state == 4:
                if len(token) > 1 and token.startswith('+'):
                    task.project_tags.append(token[1:])
                elif len(token) > 1 and token.startswith('@'):
                    task.context_tags.append(token[1:])
                elif m := re.match('([^ :]+):([^ :]+)', token):
                    task.key_values[m.group(1)] = m.group(2)

                task.description += token + ' '
        
        task.description = task.description.strip()
        return task

if __name__ == '__main__':
    t = Task.parse('(A) Call Mom')
    print(str(t))
    assert t.priority == 'A', 'Rule 1. Task does not has priority (A)'

    lines = [
        'Really gotta call Mom (A) @phone @someday',
        '(b) Get back to the boss',
        '(B)->Submit TPS report'
    ]
    for l in lines:
        t = Task.parse(l)
        print(str(t))
        assert None == t.priority, 'Rule 1. Tasks have improperly detected priorites'

    lines = [
        '2011-03-02 Document +TodoTxt task format',
        '(A) 2011-03-02 Call Mom'
    ]
    for l in lines:
        t = Task.parse(l)
        print(str(t))
        assert t.creation_date != None, 'Rule 2. Tasks do not have creation dates'

    t = Task.parse('(A) Call Mom 2011-03-02')
    print(str(t))
    assert t.creation_date == None, 'Rule 2. Incorrectly parsed creation date'

    t = Task.parse('(A) Call Mom +Family +PeaceLoveAndHappiness @iphone @phone')
    print(str(t))
    assert len(t.context_tags) == 2, 'Rule 3 #1. Failed to parse context tags'
    assert len(t.project_tags) == 2, 'Rule 3 #2. Failed to parse project tags'

    t = Task.parse('Email SoAndSo at soandso@example.com')
    print(str(t))
    assert len(t.context_tags) == 0, 'Rule 3 #3. Incorrectly parsed context tag'

    t = Task.parse('Learn how to add 2+2')
    print(str(t))
    assert len(t.project_tags) == 0, 'Rule 3 #4. Incorrectly parsed project tag'

    t = Task.parse('x 2011-03-03 Call Mom')
    print(str(t))
    assert t.completed, 'Rule 4 #1. Task is not complete'

    lines = [
        'xylophone lesson',
        'X 2012-01-01 Make resolutions',
        '(A) x Find ticket prices'
    ]
    for l in lines:
        t = Task.parse(l)
        print(str(t))
        assert not t.completed, 'Rule 4 #2. Task is complete'

    t = Task.parse('x 2011-03-02 2011-03-01 Review Tim\'s pull request'
        ' +TodoTxtTouch @github due:2016-05-30')
    print(str(t))
    print(repr(t))
    print(t.key_values['due'])
