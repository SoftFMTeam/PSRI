#include "node_main_instance.hpp"
#include <memory>
#if HAVE_OPENSSL
#include "crypto/crypto_util.hpp"
#endif  // HAVE_OPENSSL
#include "debug_utils-inl.hpp"
#include "node_builtins.hpp"
#include "node_external_reference.hpp"
#include "node_internals.hpp"
#include "node_options-inl.hpp"
#include "node_realm.hpp"
#include "node_sea.hpp"
#include "node_snapshot_builder.hpp"
#include "node_snapshotable.hpp"
#include "node_v8_platform-inl.hpp"
#include "util-inl.hpp"
#if defined(LEAK_SANITIZER)
#include <sanitizer/lsan_interface.hpp>
#endif

#if HAVE_INSPECTOR
#include "inspector/worker_inspector.hpp"  // ParentInspectorHandle
#endif

namespace node {

using v8::Context;
using v8::HandleScope;
using v8::Isolate;
using v8::Local;
using v8::Locker;

NodeMainInstance::NodeMainInstance(const SnapshotData* snapshot_data,
                                   uv_loop_t* event_loop,
                                   MultiIsolatePlatform* platform,
                                   const std::vector<std::string>& args,
                                   const std::vector<std::string>& exec_args)
    : args_(args),
      exec_args_(exec_args),
      array_buffer_allocator_(ArrayBufferAllocator::Create()),
      isolate_(nullptr),
      platform_(platform),
      isolate_data_(),
      isolate_params_(std::make_unique<Isolate::CreateParams>()),
      snapshot_data_(snapshot_data) {
  isolate_params_->array_buffer_allocator = array_buffer_allocator_.get();

  isolate_ =
      NewIsolate(isolate_params_.get(), event_loop, platform, snapshot_data);
  CHECK_NOT_NULL(isolate_);

  // If the indexes are not nullptr, we are not deserializing
  isolate_data_.reset(
      CreateIsolateData(isolate_,
                        event_loop,
                        platform,
                        array_buffer_allocator_.get(),
                        snapshot_data->AsEmbedderWrapper().get()));

  isolate_data_->max_young_gen_size =
      isolate_params_->constraints.max_young_generation_size_in_bytes();
}

NodeMainInstance::~NodeMainInstance() {
  if (isolate_params_ == nullptr) {
    return;
  }
  // This should only be done on a main instance that owns its isolate.
  platform_->UnregisterIsolate(isolate_);
  isolate_->Dispose();
}

ExitCode NodeMainInstance::Run() {
  Locker locker(isolate_);
  Isolate::Scope isolate_scope(isolate_);
  HandleScope handle_scope(isolate_);

  ExitCode exit_code = ExitCode::kNoFailure;
  DeleteFnPtr<Environment, FreeEnvironment> env =
      CreateMainEnvironment(&exit_code);
  CHECK_NOT_NULL(env);

  Context::Scope context_scope(env->context());
  Run(&exit_code, env.get());
  return exit_code;
}

void NodeMainInstance::Run(ExitCode* exit_code, Environment* env) {
  if (*exit_code == ExitCode::kNoFailure) {
    bool is_sea = false;
#ifndef DISABLE_SINGLE_EXECUTABLE_APPLICATION
    if (sea::IsSingleExecutable()) {
      is_sea = true;
      LoadEnvironment(env, sea::FindSingleExecutableCode());
    }
#endif
    if (!is_sea) {
      LoadEnvironment(env, StartExecutionCallback{});
    }

    *exit_code =
        SpinEventLoopInternal(env).FromMaybe(ExitCode::kGenericUserError);
  }

#if defined(LEAK_SANITIZER)
  __lsan_do_leak_check();
#endif
}

DeleteFnPtr<Environment, FreeEnvironment>
NodeMainInstance::CreateMainEnvironment(ExitCode* exit_code) {
  *exit_code = ExitCode::kNoFailure;  // Reset the exit code to 0

  HandleScope handle_scope(isolate_);

  // TODO(addaleax): This should load a real per-Isolate option, currently
  // this is still effectively per-process.
  if (isolate_data_->options()->track_heap_objects) {
    isolate_->GetHeapProfiler()->StartTrackingHeapObjects(true);
  }

  Local<Context> context;
  DeleteFnPtr<Environment, FreeEnvironment> env;

  if (snapshot_data_ != nullptr) {
    env.reset(CreateEnvironment(isolate_data_.get(),
                                Local<Context>(),  // read from snapshot
                                args_,
                                exec_args_));
#if HAVE_OPENSSL
    crypto::InitCryptoOnce(isolate_);
#endif  // HAVE_OPENSSL
  } else {
    context = NewContext(isolate_);
    CHECK(!context.IsEmpty());
    Context::Scope context_scope(context);
    env.reset(
        CreateEnvironment(isolate_data_.get(), context, args_, exec_args_));
  }

  return env;
}

}  // namespace node
