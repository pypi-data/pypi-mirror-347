from qtpy.QtCore import QThread
from pymodaq.control_modules.move_utility_classes import (DAQ_Move_base, comon_parameters_fun, main,
                                                          DataActuatorType, DataActuator)

from pymodaq_plugins_piezoconcept.hardware.piezoconcept.piezoconcept import PiezoConcept, Position, Time
from pymodaq_plugins_piezoconcept.utils import Config

config = Config()

# find available COM ports
import serial.tools.list_ports

ports = [str(port)[0:4] for port in list(serial.tools.list_ports.comports())]
port = config('com_port') if config('com_port') in ports else ports[0] if len(ports) > 0 else ''


class DAQ_Move_PiezoConcept(DAQ_Move_base):
    """
    Plugin to drive piezoconcpet XY (Z) stages. There is a nonlinear offset between the set position and the read
    position. It seems to bnot be problem in the sens where a given displacement is maintained. But because the read
    position is not "accurate", I've decided to ignore it and just trust the set position. So the return will be always
    strictly equal to the set position. However, if there is more that 10% difference raise a warning
    """

    axis_names = ['X', 'Y', 'Z']
    _controller_units = 'µm'
    _epsilons = [1, 1, 1]

    min_bound = -95  #*µm
    max_bound = 95  #µm
    offset = 100  #µm

    data_actuator_type = DataActuatorType.DataActuator

    params= [{'title': 'Time interval (ms):', 'name': 'time_interval', 'type': 'int', 'value': 200},
             {'title': 'Controller Info:', 'name': 'controller_id', 'type': 'text', 'value': '', 'readonly': True},
             {'title': 'COM Port:', 'name': 'com_port', 'type': 'list', 'limits': ports, 'value': port},
             ] + comon_parameters_fun(axis_names=axis_names)

    def ini_attributes(self):
        self.controller: PiezoConcept = None

    def ini_stage(self, controller=None):
        """

        """
        if self.is_master:
            self.controller = PiezoConcept()
        else:
            self.controller = controller

        controller_id = self.do_init()

        info = controller_id
        initialized = True
        return info, initialized

    def do_init(self) -> str:
        if self.is_master:
            self.controller.init_communication(self.settings['com_port'])

        controller_id = self.controller.get_controller_infos()
        self.settings.child('controller_id').setValue(controller_id)

        self.settings.child('bounds', 'is_bounds').setValue(True)
        self.settings.child('bounds', 'min_bound').setValue(self.min_bound)
        self.settings.child('bounds', 'max_bound').setValue(self.max_bound)
        self.settings.child('scaling', 'use_scaling').setValue(True)
        self.settings.child('scaling', 'offset').setValue(self.offset)
        self.move_abs(DataActuator(data=0, units=self.axis_unit))
        return controller_id

    def close(self):
        """
            close the current instance of Piezo instrument.
        """
        if self.controller is not None:
            self.move_abs(DataActuator(0, units='um'))
            QThread.msleep(1000)
            self.controller.close_communication()
        self.controller = None

    def get_actuator_value(self) -> DataActuator:
        """
        """
        pos: Position = self.controller.get_position(self.axis_name)
        position = DataActuator(data=pos.pos,
                                units='nm' if pos.unit == 'n' else 'um')
        position = self.get_position_with_scaling(position)
        self.current_value = self.target_value  #should be pos but not precise enough conpared to set position
        return self.target_value

    def move_abs(self, position: DataActuator):
        """

        Parameters
        ----------
        position: (float) target position of the given axis in um (or scaled units)

        Returns
        -------

        """
        position = self.check_bound(position)  #limits the position within the specified bounds (-100,100)
        self.target_value = position
        position = self.set_position_with_scaling(position)

        #get positions in controller units
        pos = Position(self.axis_name, position.value('nm'), unit='n')
        out = self.controller.move_axis('ABS', pos)
        QThread.msleep(50)  # to make sure the closed loop converged

    def move_rel(self, position: DataActuator):
        """ Make the hardware relative move of the Piezo instrument from the given position
        """
        position = self.check_bound(self.current_value+position)-self.current_value
        self.target_value = position+self.current_value

        position = self.set_position_relative_with_scaling(position)

        pos = Position(self.axis_name, position.value('nm'), unit='n')
        out = self.controller.move_axis('REL', pos)
        QThread.msleep(50)  # to make sure the closed loop converged

    def move_home(self):
        """
            Move to the absolute vlue 100 corresponding the default point of the Piezo instrument.

            See Also
            --------
            DAQ_Move_base.move_abs
        """
        self.move_abs(DataActuator(data=100, units='um'))
        # put the axis on the middle position so 100µm

    def stop_motion(self):
        """
        Call the specific move_done function (depending on the hardware).

        See Also
        --------
        move_done
        """
        self.move_done()


if __name__ == '__main__':
    main(__file__, init=False)
