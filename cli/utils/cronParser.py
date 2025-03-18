import re

class CronParser:
    def __init__(self, expression):
        self.expression = expression
        self.parts = []
        self.field_names = ['minute', 'hour', 'day of month', 'month', 'day of week']
        self.field_ranges = [
            (0, 59),    # minute
            (0, 23),    # hour
            (1, 31),    # day of month
            (1, 12),   # month
            (0, 6)      # day of week (0=Sunday)
        ]
        self.parse()

    def parse(self):
        # 拆分表达式为5个部分
        parts = self.expression.split()
        if len(parts) != 5:
            raise ValueError("Invalid cron expression. Must contain exactly 5 fields.")

        for i, part in enumerate(parts):
            self.parts.append(self._parse_field(part, *self.field_ranges[i]))

    def _parse_field(self, field_str, min_val, max_val):
        # 处理特殊字符 *
        if field_str == '*':
            return list(range(min_val, max_val + 1))

        # 处理逗号分隔的列表
        if ',' in field_str:
            values = []
            for item in field_str.split(','):
                values.extend(self._parse_item(item, min_val, max_val))
            return sorted(list(set(values)))  # 去重并排序

        # 处理单个项目
        return self._parse_item(field_str, min_val, max_val)

    def _parse_item(self, item, min_val, max_val):
        # 处理步长值（例如 */5 或 1-30/3）
        step = 1
        if '/' in item:
            item, step = item.split('/')
            step = int(step)
            if step < 1:
                raise ValueError(f"Step value must be positive integer: {item}")

        # 处理范围（例如 1-5）
        if '-' in item:
            start, end = item.split('-')
            start = self._validate_value(int(start), min_val, max_val)
            end = self._validate_value(int(end), min_val, max_val)
            if start > end:
                raise ValueError(f"Invalid range {start}-{end}")
            values = list(range(start, end + 1, step))
        elif item == '*':
            values = list(range(min_val, max_val + 1, step))
        else:
            # 处理单个值
            value = self._validate_value(int(item), min_val, max_val)
            values = [value]

        # 应用步长
        if step > 1:
            values = values[::step]

        return values

    def _validate_value(self, value, min_val, max_val):
        if value < min_val or value > max_val:
            raise ValueError(f"Value {value} out of range ({min_val}-{max_val})")
        return value

    def get_execution_times(self):
        return {name: values for name, values in zip(self.field_names, self.parts)}

    def __str__(self):
        result = []
        for name, values in zip(self.field_names, self.parts):
            result.append(f"{name.ljust(14)}{' '.join(map(str, values))}")
        return '\n'.join(result)
