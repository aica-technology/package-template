#pragma once

#include <modulo_controllers/RobotControllerInterface.hpp>

namespace template_controller_package {

class TemplateController : public modulo_controllers::RobotControllerInterface {
public:
  TemplateController();

  CallbackReturn add_interfaces() override;
  CallbackReturn on_configure() override;
  CallbackReturn on_activate() override;
  CallbackReturn on_deactivate() override;

private:
  controller_interface::return_type evaluate(const rclcpp::Time& time, const std::chrono::nanoseconds& period) override;

  bool
  on_validate_parameter_callback(const std::shared_ptr<state_representation::ParameterInterface>& parameter) override;
};

}// namespace template_controller_package
