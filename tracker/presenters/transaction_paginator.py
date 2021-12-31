MAX_PAGES_SHOWN = 3
MIN_PAGE = 1

class TransactionPaginator:
    def __init__(self, total, current_page):
        assert current_page >= MIN_PAGE, "The current page must be positive"
        assert current_page <= total, "The current page cannot be greater than the total number of pages"

        self.total = total
        self.current_page = current_page

    def page_numbers_to_show(self):
        result = []

        if self.current_page == MIN_PAGE:
            for i in range(MAX_PAGES_SHOWN):
                page_number = self.current_page + i
                if page_number > self.total:
                    break

                result.append(page_number)
        elif self.current_page == self.total:
            for i in range(MAX_PAGES_SHOWN):
                page_number = self.current_page - i
                if page_number < MIN_PAGE:
                    break

                result.insert(0, page_number)
        else:
            result = [self.current_page-1, self.current_page, self.current_page+1]

        return result

    def previous_page(self):
        if self.current_page - 1 >= MIN_PAGE:
            return self.current_page - 1
        else:
            return MIN_PAGE

    def next_page(self):
        if self.current_page + 1 > self.total:
            return self.total
        else:
            return self.current_page + 1

    def is_previous_button_disabled(self):
        return self.current_page == MIN_PAGE

    def is_next_button_disabled(self):
        return self.current_page == self.total
