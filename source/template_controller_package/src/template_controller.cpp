#include "template_controller_package/template_controller.hpp"

#include <hardware_interface/types/hardware_interface_type_values.hpp>

using namespace state_representation;

namespace template_controller_package {

TemplateController::TemplateController()
    : modulo_controllers::RobotControllerInterface(true, hardware_interface::HW_IF_POSITION) {}

rclcpp_lifecycle::node_interfaces::LifecycleNodeInterface::CallbackReturn TemplateController::add_interfaces() {
  auto ret = modulo_controllers::RobotControllerInterface::add_interfaces();
  if (ret != CallbackReturn::SUCCESS) {
    return ret;
  }
  // declaration of parameters, interfaces, inputs, outputs, etc
  return CallbackReturn::SUCCESS;
}

rclcpp_lifecycle::node_interfaces::LifecycleNodeInterface::CallbackReturn TemplateController::on_configure() {
  auto ret = modulo_controllers::RobotControllerInterface::on_configure();
  if (ret != CallbackReturn::SUCCESS) {
    return ret;
  }
  // configuration steps before activation
  return CallbackReturn::SUCCESS;
}

rclcpp_lifecycle::node_interfaces::LifecycleNodeInterface::CallbackReturn TemplateController::on_activate() {
  auto ret = modulo_controllers::RobotControllerInterface::on_activate();
  if (ret != CallbackReturn::SUCCESS) {
    return ret;
  }
  // activation steps before running
  return CallbackReturn::SUCCESS;
}

rclcpp_lifecycle::node_interfaces::LifecycleNodeInterface::CallbackReturn TemplateController::on_deactivate() {
  auto ret = modulo_controllers::RobotControllerInterface::on_deactivate();
  if (ret != CallbackReturn::SUCCESS) {
    return ret;
  }
  // deactivation steps
  return CallbackReturn::SUCCESS;
}

controller_interface::return_type TemplateController::evaluate(const rclcpp::Time&, const std::chrono::nanoseconds&) {
  // implementation of a control logic
  return controller_interface::return_type::OK;
}

bool TemplateController::on_validate_parameter_callback(const std::shared_ptr<ParameterInterface>& parameter) {
  // validation of parameters (if needed)
  return modulo_controllers::RobotControllerInterface::on_validate_parameter_callback(parameter);
}

}// namespace template_controller_package

#include "pluginlib/class_list_macros.hpp"

PLUGINLIB_EXPORT_CLASS(template_controller_package::TemplateController, controller_interface::ControllerInterface)
