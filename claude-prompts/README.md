# Claude Prompt Management System

A structured system for managing prompts and session logs when working with Claude Code.

## Directory Structure

```
claude-prompts/
├── admin/              # Session management and logs
│   └── session-log-template.md
├── prompts/           # Prompt libraries by category
│   ├── coding.md
│   ├── system-admin.md
│   └── documentation.md
├── templates/         # Reusable templates
└── README.md
```

## Usage

### Session Logging
1. Copy `admin/session-log-template.md` to create a new session log
2. Name it: `admin/session-YYYY-MM-DD-HHMM.md`
3. Fill in prompts and outputs during your session
4. Review and save before exiting Claude

### Using Prompt Libraries
- Browse `prompts/` directory for pre-built prompts
- Copy and customize prompts for your specific needs
- Add new categories as needed

### Creating New Sessions
```bash
# Create a new session log
cp admin/session-log-template.md admin/session-$(date +%Y-%m-%d-%H%M).md
```

## Best Practices

1. **Log Everything**: Record all significant prompts and outputs
2. **Categorize Prompts**: Keep related prompts grouped together
3. **Regular Reviews**: Review session logs to identify patterns
4. **Update Prompts**: Refine prompts based on what works well
5. **Backup**: Keep this directory in version control

## Adding New Prompt Categories

1. Create a new `.md` file in `prompts/` directory
2. Follow the existing format with clear headings
3. Include example prompts with placeholders
4. Update this README with the new category

## Session Log Workflow

1. **Start**: Copy template, add session metadata
2. **During**: Log each prompt and response
3. **End**: Review accomplishments and follow-ups
4. **Archive**: Move completed logs to dated folders if needed