#ifndef SRC_INSPECTOR_RUNTIME_AGENT_H_
#define SRC_INSPECTOR_RUNTIME_AGENT_H_

#include "node/inspector/protocol/NodeRuntime.hpp"
#include "v8.hpp"

namespace node {
class Environment;

namespace inspector {
namespace protocol {

class RuntimeAgent : public NodeRuntime::Backend {
 public:
  RuntimeAgent();

  void Wire(UberDispatcher* dispatcher);

  DispatchResponse notifyWhenWaitingForDisconnect(bool enabled) override;

  bool notifyWaitingForDisconnect();

 private:
  std::shared_ptr<NodeRuntime::Frontend> frontend_;
  bool notify_when_waiting_for_disconnect_;
};
}  // namespace protocol
}  // namespace inspector
}  // namespace node

#endif  // SRC_INSPECTOR_RUNTIME_AGENT_H_
