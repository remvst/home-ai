from output import Output


class Stdout(Output):

    def output(self, string):
        print string
