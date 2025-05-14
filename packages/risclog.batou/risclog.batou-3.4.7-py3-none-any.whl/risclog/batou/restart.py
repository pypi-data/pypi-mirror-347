import batou


class Restart(batou.component.Component):

    service = batou.component.Attribute()
    namevar = 'service'

    def verify(self):
        if self.environment.name in ('testing',):
            raise batou.UpdateNeeded()

    def update(self):
        self.cmd(f'sudo systemctl restart {self.service}.service')
