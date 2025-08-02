# Deletion Audit Trail and Soft-Delete Features

This Django application implements production-level audit trail and soft-delete functionality for data security and accountability.

## Features Implemented

### 1. Deletion Log Model (`core.models.DeletionLog`)
- Records who deleted each item
- When the deletion occurred  
- What data was deleted (JSON snapshot)
- Tracks model name and object ID

### 2. Soft Delete Base Model (`core.models.SoftDeleteModel`)
- Abstract base class for models requiring soft-delete
- Fields: `is_deleted`, `deleted_at`, `deleted_by`
- Methods: `soft_delete()`, `restore()`, `as_dict()`

### 3. Enhanced Admin Interface (`core.admin.SoftDeleteAdmin`)
- Shows both active and deleted items
- Custom actions: "Soft delete", "Restore", "Hard delete"
- Only superusers can permanently delete items
- Automatic audit trail creation

### 4. Management Command (`python manage.py manage_deletions`)
- List deletion logs: `--list-logs`
- Filter by model: `--model ModelName`
- Filter by user: `--user username`
- Restore deleted items: `--restore <log_id>`

## Models Updated with Soft Delete

### Students App
- `Admission` - Student admission records
- `Marksheet` - Academic records
- `Certificate` - Achievement certificates

### Core App
- `ContactMessage` - Contact form submissions

## Usage Examples

### Admin Interface
1. Navigate to Django Admin
2. Select items to delete
3. Choose "Soft delete selected items" action
4. Items are marked as deleted but preserved
5. Use "Restore selected items" to recover
6. View audit trail in "Deletion logs"

### Command Line Management
```bash
# List all deletion logs
python manage.py manage_deletions --list-logs

# List logs for specific model
python manage.py manage_deletions --list-logs --model Admission

# List logs by user
python manage.py manage_deletions --list-logs --user admin

# Restore deleted item by log ID
python manage.py manage_deletions --restore 123
```

### Programmatic Usage
```python
# Soft delete with user tracking
admission.soft_delete(user=request.user)

# Restore deleted item
admission.restore()

# Query only active items
active_admissions = Admission.objects.filter(is_deleted=False)

# Query all items (including deleted)
all_admissions = Admission.objects.all()
```

## Security Features

### Data Protection
- Items are never truly lost (soft delete)
- Complete audit trail of all deletions
- JSON snapshots preserve original data
- User accountability for all changes

### Access Control
- Hard delete restricted to superusers only
- Audit logs are read-only in admin
- Automatic user tracking on deletions
- Timestamps for all deletion events

### Recovery Options
- Admin interface for easy restoration
- Command-line tools for bulk operations
- Programmatic restore methods
- Data integrity preservation

## Database Migrations

After implementing these features, run:
```bash
python manage.py makemigrations
python manage.py migrate
```

## Best Practices

### For Developers
- Always use `soft_delete(user=request.user)` instead of `delete()`
- Filter queries with `is_deleted=False` for public views
- Use admin actions for bulk operations
- Review deletion logs regularly

### For Administrators
- Use soft delete for routine cleanup
- Reserve hard delete for privacy compliance
- Monitor deletion logs for suspicious activity
- Train staff on restore procedures

## Troubleshooting

### Common Issues
- **Migration errors**: Ensure all apps are in INSTALLED_APPS
- **Import errors**: Check that core app is properly configured
- **Permission errors**: Verify user has appropriate admin access
- **Restore failures**: Check that item exists and is soft-deleted

### Performance Considerations
- Add database indexes on `is_deleted` fields (already included)
- Archive old deletion logs periodically
- Use pagination for large deletion log queries
- Consider cleanup jobs for very old soft-deleted items

## Future Enhancements

### Potential Additions
- Email notifications for deletions
- Bulk restore operations
- Automated backup to external storage
- Role-based deletion permissions
- Scheduled hard delete of old items
- API endpoints for deletion management

This implementation provides enterprise-grade data protection while maintaining ease of use for administrators and developers.
