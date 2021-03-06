from pprint import pprint

from pyfrc.test_support import controller
import robotmap


def test_driving(hal_data: controller.hal_data, control: controller.TestController, fake_time, robot):
    def tController(time):
        hal_data['joysticks'][robotmap.joystick.port]['buttons'][1] = (time // 4) % 2  # mashing a button
        hal_data['joysticks'][robotmap.joystick.port]['buttons'][2] = (time // 8) % 2  # mashing b button
        if time < 10:
            hal_data['joysticks'][robotmap.joystick.port]['axes'][robotmap.joystick.forwardAxis] = (time - 5) / 5.0
        elif time < 20:
            hal_data['joysticks'][robotmap.joystick.port]['axes'][robotmap.joystick.forwardAxis] = (time - 15) / -5.0
            hal_data['joysticks'][robotmap.joystick.port]['axes'][robotmap.joystick.steeringAxis] = (time - 15) / 5.0
        elif time < 30:
            hal_data['joysticks'][robotmap.joystick.port]['axes'][robotmap.joystick.steeringAxis] = (time - 25) / -5.0
        else:
            return False
        return True

    control.set_operator_control(enabled=True)
    control.run_test(tController)
    assert int(fake_time.get()) == 30


# def test_testing(hal_data: controller.hal_data, control: controller.TestController, fake_time, robot):
#
#     def tController(time):
#         hal_data['joysticks'][robotmap.joystick.port]['axes'][robotmap.joystick.forwardAxis] = 0.1
#         hal_data['joysticks'][robotmap.joystick.port]['axes'][robotmap.joystick.steeringAxis] = 0.5
#         for x in hal_data['CAN']:
#             print(x, hal_data['CAN'][x]['value'])
#         if time > 2:
#             return False
#         return True
#
#     control.set_operator_control(enabled=True)
#     control.run_test(tController)
#
#     for x in hal_data:
#         print(x)
#
#     print('==== CAN ====')
#     for x in hal_data['CAN']:
#         print(x, hal_data['CAN'][x]['value'])
#         # pprint(hal_data['CAN'][x])
#     assert False
