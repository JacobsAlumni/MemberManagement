import unicodecsv
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse


def export_as_csv_action(description="Export selected objects as CSV file",
                         fields=None, exclude=None, header=True):
    """
    This function returns an export csv action
    'fields' and 'exclude' work like in django ModelForm
    'header' is whether or not to output the column names as the first row
    """

    def get_model_prop(modeladmin, obj, field):
        try:
            try:
                # get the attribute directly from the instance
                attr = getattr(obj, field)
                return attr() if callable(attr) else attr
            except AttributeError:
                # else return an error
                attr = getattr(modeladmin, field)
                return attr(obj)
        except ObjectDoesNotExist:
            return None

    def export_as_csv(modeladmin, request, queryset):
        opts = modeladmin.model._meta

        if not fields:
            field_names = [field.name for field in opts.fields]
        else:
            field_names = fields

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % str(
            opts).replace('.', '_')

        writer = unicodecsv.writer(response, encoding='utf-8')
        if header:
            writer.writerow(field_names)
        for obj in queryset:
            row = [get_model_prop(modeladmin, obj, field) for field in
                   field_names]
            writer.writerow(row)
        return response

    export_as_csv.short_description = description
    return export_as_csv
