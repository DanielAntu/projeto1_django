def is_positive_number(value):
    try:
        number_string = float(value)
    except (ValueError, TypeError) as e:
        return False
    
    return number_string > 0

if __name__ == '__main__':
    print(is_positive_number('10'))
    print(is_positive_number('-10'))