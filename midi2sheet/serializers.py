from rest_framework import serializers
from midi2sheet.models import Merge, Sheet, MidiToSheet


class MidiToSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = MidiToSheet
        fields = ('base_dir',)

class MergeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merge
        # fields = '__all__'
        fields = ('melo_file', 'acco_file', 'output_file')

class SheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sheet
        # fields = '__all__'
        fields = ('tool_dir', 'input_file', 'output_dir')