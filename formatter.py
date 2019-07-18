class Formatter(object):

    @staticmethod
    def format_answers(results):
        answers = []
        for result in results:
            answers.append(result['message'])
        return ' '.join(answers)