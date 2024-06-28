from django.db import models
from modelcluster.fields import ParentalKey

from wagtail.models import Page, Orderable
from wagtail.fields import StreamField
from wagtail.blocks import CharBlock, RichTextBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.panels import FieldPanel, InlinePanel


class HomePage(Page):
    body = StreamField(
        [
            ("title", CharBlock(form_classname="main title")),
            ("paragraph", RichTextBlock()),
            ("image", ImageChooserBlock()),
        ],
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [FieldPanel("body")]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["schedules"] = SchedulePage.objects.child_of(self).live()
        return context


class TrainingSlot(models.Model):
    weekdkay = models.CharField(max_length=20)
    start_time = models.TimeField()
    end_time = models.TimeField()
    description = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

    class Meta:
        abstract = True


class SchedulePageTrainingSlot(Orderable, TrainingSlot):
    page = ParentalKey(
        "SchedulePage", on_delete=models.CASCADE, related_name="slots", blank=True
    )


class SchedulePage(Page):
    content_panels = Page.content_panels + [InlinePanel("slots", label="Timeslots")]
