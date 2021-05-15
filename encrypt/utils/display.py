class BetterDisplay():
    def bigText(texts, path=None):
        big_text = ""
        c = 0
        for text in texts:
            if c != 4:
                big_text += f"{text}\n"
            else:
                big_text += f"{path}\n"
            c += 1
        return big_text


    def filename(string, n=50):
        """
        :param string: str to short
        :param n: number to short
        :return: string
        short a string, used to display long strings
        """
        cut_string = ""
        if len(string) > 50:
            if n > len(string):
                n = len(string)
            cut_string = string[:n:1]
            if cut_string != string:
                cut_string += "..."
        else:
            cut_string = string
        return cut_string