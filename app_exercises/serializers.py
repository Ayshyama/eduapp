from rest_framework import serializers


class TestAnswerSerializer(serializers.Serializer):
    answer = serializers.JSONField()

    def validate_answer(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError('answer must be a dict')
        for key, val in value.items():
            if not isinstance(key, str) or not type(val) is bool:
                break
            if not key[:12] == 'name_answer_' or not key[12:].isdigit():
                break
        else:
            return value
        raise serializers.ValidationError('answer must be a dict with keys: name_answer_1, name_answer_2, etc.')


class CodeAnswerSerializer(serializers.Serializer):
    answer = serializers.CharField()

    def validate_answer(self, value):
        if not isinstance(value, str):
            raise serializers.ValidationError('answer must be a string')
        return value
