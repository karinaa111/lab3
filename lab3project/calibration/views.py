from django.shortcuts import render
from .forms import CalibrationForm
import re

WORD_DIGITS = {
    'one': '1', 'two': '2', 'three': '3', 'four': '4',
    'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9'
}


def get_calibration_value_part1(line):
    digits = [ch for ch in line if ch.isdigit()]
    if not digits:
        return 0
    return int(digits[0] + digits[-1])


def get_calibration_value_part2(line):
    # Find all digits (real or spelled), allowing overlaps (e.g. "twone" -> 2,1)
    pattern = r'(?=(\d|one|two|three|four|five|six|seven|eight|nine))'
    matches = re.findall(pattern, line)
    if not matches:
        return 0
    def to_digit(m):
        return WORD_DIGITS.get(m, m)
    first = to_digit(matches[0])
    last = to_digit(matches[-1])
    return int(first + last)


def analyze(text):
    lines = [l for l in text.strip().splitlines() if l.strip()]
    results = []
    total1 = 0
    total2 = 0
    for line in lines:
        v1 = get_calibration_value_part1(line)
        v2 = get_calibration_value_part2(line)
        total1 += v1
        total2 += v2
        results.append({'line': line, 'val1': v1, 'val2': v2})
    return results, total1, total2


def index(request):
    form = CalibrationForm()
    context = {'form': form}

    if request.method == 'POST':
        form = CalibrationForm(request.POST, request.FILES)
        if form.is_valid():
            if request.FILES.get('data_file'):
                raw = request.FILES['data_file'].read().decode('utf-8', errors='ignore')
            else:
                raw = form.cleaned_data['data_text']

            results, total1, total2 = analyze(raw)

            context = {
                'form': form,
                'results': results,
                'total1': total1,
                'total2': total2,
                'total_lines': len(results),
                'analyzed': True,
            }

    return render(request, 'calibration/index.html', context)
