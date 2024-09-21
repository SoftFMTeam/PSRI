// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: versions.proto

#include "versions.pb.hpp"

#include <algorithm>

#include <google/protobuf/io/coded_stream.hpp>
#include <google/protobuf/extension_set.hpp>
#include <google/protobuf/wire_format_lite.hpp>
#include <google/protobuf/descriptor.hpp>
#include <google/protobuf/generated_message_reflection.hpp>
#include <google/protobuf/reflection_ops.hpp>
#include <google/protobuf/wire_format.hpp>
// @@protoc_insertion_point(includes)
#include <google/protobuf/port_def.inc>

PROTOBUF_PRAGMA_INIT_SEG
namespace opencv_tensorflow {
constexpr VersionDef::VersionDef(
  ::PROTOBUF_NAMESPACE_ID::internal::ConstantInitialized)
  : bad_consumers_()
  , _bad_consumers_cached_byte_size_(0)
  , producer_(0)
  , min_consumer_(0){}
struct VersionDefDefaultTypeInternal {
  constexpr VersionDefDefaultTypeInternal()
    : _instance(::PROTOBUF_NAMESPACE_ID::internal::ConstantInitialized{}) {}
  ~VersionDefDefaultTypeInternal() {}
  union {
    VersionDef _instance;
  };
};
PROTOBUF_ATTRIBUTE_NO_DESTROY PROTOBUF_CONSTINIT VersionDefDefaultTypeInternal _VersionDef_default_instance_;
}  // namespace opencv_tensorflow
static ::PROTOBUF_NAMESPACE_ID::Metadata file_level_metadata_versions_2eproto[1];
static constexpr ::PROTOBUF_NAMESPACE_ID::EnumDescriptor const** file_level_enum_descriptors_versions_2eproto = nullptr;
static constexpr ::PROTOBUF_NAMESPACE_ID::ServiceDescriptor const** file_level_service_descriptors_versions_2eproto = nullptr;

const uint32_t TableStruct_versions_2eproto::offsets[] PROTOBUF_SECTION_VARIABLE(protodesc_cold) = {
  ~0u,  // no _has_bits_
  PROTOBUF_FIELD_OFFSET(::opencv_tensorflow::VersionDef, _internal_metadata_),
  ~0u,  // no _extensions_
  ~0u,  // no _oneof_case_
  ~0u,  // no _weak_field_map_
  ~0u,  // no _inlined_string_donated_
  PROTOBUF_FIELD_OFFSET(::opencv_tensorflow::VersionDef, producer_),
  PROTOBUF_FIELD_OFFSET(::opencv_tensorflow::VersionDef, min_consumer_),
  PROTOBUF_FIELD_OFFSET(::opencv_tensorflow::VersionDef, bad_consumers_),
};
static const ::PROTOBUF_NAMESPACE_ID::internal::MigrationSchema schemas[] PROTOBUF_SECTION_VARIABLE(protodesc_cold) = {
  { 0, -1, -1, sizeof(::opencv_tensorflow::VersionDef)},
};

static ::PROTOBUF_NAMESPACE_ID::Message const * const file_default_instances[] = {
  reinterpret_cast<const ::PROTOBUF_NAMESPACE_ID::Message*>(&::opencv_tensorflow::_VersionDef_default_instance_),
};

const char descriptor_table_protodef_versions_2eproto[] PROTOBUF_SECTION_VARIABLE(protodesc_cold) =
  "\n\016versions.proto\022\021opencv_tensorflow\"K\n\nV"
  "ersionDef\022\020\n\010producer\030\001 \001(\005\022\024\n\014min_consu"
  "mer\030\002 \001(\005\022\025\n\rbad_consumers\030\003 \003(\005B/\n\030org."
  "tensorflow.frameworkB\016VersionsProtosP\001\370\001"
  "\001b\006proto3"
  ;
static ::PROTOBUF_NAMESPACE_ID::internal::once_flag descriptor_table_versions_2eproto_once;
const ::PROTOBUF_NAMESPACE_ID::internal::DescriptorTable descriptor_table_versions_2eproto = {
  false, false, 169, descriptor_table_protodef_versions_2eproto, "versions.proto",
  &descriptor_table_versions_2eproto_once, nullptr, 0, 1,
  schemas, file_default_instances, TableStruct_versions_2eproto::offsets,
  file_level_metadata_versions_2eproto, file_level_enum_descriptors_versions_2eproto, file_level_service_descriptors_versions_2eproto,
};
PROTOBUF_ATTRIBUTE_WEAK const ::PROTOBUF_NAMESPACE_ID::internal::DescriptorTable* descriptor_table_versions_2eproto_getter() {
  return &descriptor_table_versions_2eproto;
}

// Force running AddDescriptors() at dynamic initialization time.
PROTOBUF_ATTRIBUTE_INIT_PRIORITY static ::PROTOBUF_NAMESPACE_ID::internal::AddDescriptorsRunner dynamic_init_dummy_versions_2eproto(&descriptor_table_versions_2eproto);
namespace opencv_tensorflow {

// ===================================================================

class VersionDef::_Internal {
 public:
};

VersionDef::VersionDef(::PROTOBUF_NAMESPACE_ID::Arena* arena,
                         bool is_message_owned)
  : ::PROTOBUF_NAMESPACE_ID::Message(arena, is_message_owned),
  bad_consumers_(arena) {
  SharedCtor();
  if (!is_message_owned) {
    RegisterArenaDtor(arena);
  }
  // @@protoc_insertion_point(arena_constructor:opencv_tensorflow.VersionDef)
}
VersionDef::VersionDef(const VersionDef& from)
  : ::PROTOBUF_NAMESPACE_ID::Message(),
      bad_consumers_(from.bad_consumers_) {
  _internal_metadata_.MergeFrom<::PROTOBUF_NAMESPACE_ID::UnknownFieldSet>(from._internal_metadata_);
  ::memcpy(&producer_, &from.producer_,
    static_cast<size_t>(reinterpret_cast<char*>(&min_consumer_) -
    reinterpret_cast<char*>(&producer_)) + sizeof(min_consumer_));
  // @@protoc_insertion_point(copy_constructor:opencv_tensorflow.VersionDef)
}

inline void VersionDef::SharedCtor() {
::memset(reinterpret_cast<char*>(this) + static_cast<size_t>(
    reinterpret_cast<char*>(&producer_) - reinterpret_cast<char*>(this)),
    0, static_cast<size_t>(reinterpret_cast<char*>(&min_consumer_) -
    reinterpret_cast<char*>(&producer_)) + sizeof(min_consumer_));
}

VersionDef::~VersionDef() {
  // @@protoc_insertion_point(destructor:opencv_tensorflow.VersionDef)
  if (GetArenaForAllocation() != nullptr) return;
  SharedDtor();
  _internal_metadata_.Delete<::PROTOBUF_NAMESPACE_ID::UnknownFieldSet>();
}

inline void VersionDef::SharedDtor() {
  GOOGLE_DCHECK(GetArenaForAllocation() == nullptr);
}

void VersionDef::ArenaDtor(void* object) {
  VersionDef* _this = reinterpret_cast< VersionDef* >(object);
  (void)_this;
}
void VersionDef::RegisterArenaDtor(::PROTOBUF_NAMESPACE_ID::Arena*) {
}
void VersionDef::SetCachedSize(int size) const {
  _cached_size_.Set(size);
}

void VersionDef::Clear() {
// @@protoc_insertion_point(message_clear_start:opencv_tensorflow.VersionDef)
  uint32_t cached_has_bits = 0;
  // Prevent compiler warnings about cached_has_bits being unused
  (void) cached_has_bits;

  bad_consumers_.Clear();
  ::memset(&producer_, 0, static_cast<size_t>(
      reinterpret_cast<char*>(&min_consumer_) -
      reinterpret_cast<char*>(&producer_)) + sizeof(min_consumer_));
  _internal_metadata_.Clear<::PROTOBUF_NAMESPACE_ID::UnknownFieldSet>();
}

const char* VersionDef::_InternalParse(const char* ptr, ::PROTOBUF_NAMESPACE_ID::internal::ParseContext* ctx) {
#define CHK_(x) if (PROTOBUF_PREDICT_FALSE(!(x))) goto failure
  while (!ctx->Done(&ptr)) {
    uint32_t tag;
    ptr = ::PROTOBUF_NAMESPACE_ID::internal::ReadTag(ptr, &tag);
    switch (tag >> 3) {
      // int32 producer = 1;
      case 1:
        if (PROTOBUF_PREDICT_TRUE(static_cast<uint8_t>(tag) == 8)) {
          producer_ = ::PROTOBUF_NAMESPACE_ID::internal::ReadVarint32(&ptr);
          CHK_(ptr);
        } else
          goto handle_unusual;
        continue;
      // int32 min_consumer = 2;
      case 2:
        if (PROTOBUF_PREDICT_TRUE(static_cast<uint8_t>(tag) == 16)) {
          min_consumer_ = ::PROTOBUF_NAMESPACE_ID::internal::ReadVarint32(&ptr);
          CHK_(ptr);
        } else
          goto handle_unusual;
        continue;
      // repeated int32 bad_consumers = 3;
      case 3:
        if (PROTOBUF_PREDICT_TRUE(static_cast<uint8_t>(tag) == 26)) {
          ptr = ::PROTOBUF_NAMESPACE_ID::internal::PackedInt32Parser(_internal_mutable_bad_consumers(), ptr, ctx);
          CHK_(ptr);
        } else if (static_cast<uint8_t>(tag) == 24) {
          _internal_add_bad_consumers(::PROTOBUF_NAMESPACE_ID::internal::ReadVarint32(&ptr));
          CHK_(ptr);
        } else
          goto handle_unusual;
        continue;
      default:
        goto handle_unusual;
    }  // switch
  handle_unusual:
    if ((tag == 0) || ((tag & 7) == 4)) {
      CHK_(ptr);
      ctx->SetLastTag(tag);
      goto message_done;
    }
    ptr = UnknownFieldParse(
        tag,
        _internal_metadata_.mutable_unknown_fields<::PROTOBUF_NAMESPACE_ID::UnknownFieldSet>(),
        ptr, ctx);
    CHK_(ptr != nullptr);
  }  // while
message_done:
  return ptr;
failure:
  ptr = nullptr;
  goto message_done;
#undef CHK_
}

uint8_t* VersionDef::_InternalSerialize(
    uint8_t* target, ::PROTOBUF_NAMESPACE_ID::io::EpsCopyOutputStream* stream) const {
  // @@protoc_insertion_point(serialize_to_array_start:opencv_tensorflow.VersionDef)
  uint32_t cached_has_bits = 0;
  (void) cached_has_bits;

  // int32 producer = 1;
  if (this->_internal_producer() != 0) {
    target = stream->EnsureSpace(target);
    target = ::PROTOBUF_NAMESPACE_ID::internal::WireFormatLite::WriteInt32ToArray(1, this->_internal_producer(), target);
  }

  // int32 min_consumer = 2;
  if (this->_internal_min_consumer() != 0) {
    target = stream->EnsureSpace(target);
    target = ::PROTOBUF_NAMESPACE_ID::internal::WireFormatLite::WriteInt32ToArray(2, this->_internal_min_consumer(), target);
  }

  // repeated int32 bad_consumers = 3;
  {
    int byte_size = _bad_consumers_cached_byte_size_.load(std::memory_order_relaxed);
    if (byte_size > 0) {
      target = stream->WriteInt32Packed(
          3, _internal_bad_consumers(), byte_size, target);
    }
  }

  if (PROTOBUF_PREDICT_FALSE(_internal_metadata_.have_unknown_fields())) {
    target = ::PROTOBUF_NAMESPACE_ID::internal::WireFormat::InternalSerializeUnknownFieldsToArray(
        _internal_metadata_.unknown_fields<::PROTOBUF_NAMESPACE_ID::UnknownFieldSet>(::PROTOBUF_NAMESPACE_ID::UnknownFieldSet::default_instance), target, stream);
  }
  // @@protoc_insertion_point(serialize_to_array_end:opencv_tensorflow.VersionDef)
  return target;
}

size_t VersionDef::ByteSizeLong() const {
// @@protoc_insertion_point(message_byte_size_start:opencv_tensorflow.VersionDef)
  size_t total_size = 0;

  uint32_t cached_has_bits = 0;
  // Prevent compiler warnings about cached_has_bits being unused
  (void) cached_has_bits;

  // repeated int32 bad_consumers = 3;
  {
    size_t data_size = ::PROTOBUF_NAMESPACE_ID::internal::WireFormatLite::
      Int32Size(this->bad_consumers_);
    if (data_size > 0) {
      total_size += 1 +
        ::PROTOBUF_NAMESPACE_ID::internal::WireFormatLite::Int32Size(
            static_cast<int32_t>(data_size));
    }
    int cached_size = ::PROTOBUF_NAMESPACE_ID::internal::ToCachedSize(data_size);
    _bad_consumers_cached_byte_size_.store(cached_size,
                                    std::memory_order_relaxed);
    total_size += data_size;
  }

  // int32 producer = 1;
  if (this->_internal_producer() != 0) {
    total_size += ::PROTOBUF_NAMESPACE_ID::internal::WireFormatLite::Int32SizePlusOne(this->_internal_producer());
  }

  // int32 min_consumer = 2;
  if (this->_internal_min_consumer() != 0) {
    total_size += ::PROTOBUF_NAMESPACE_ID::internal::WireFormatLite::Int32SizePlusOne(this->_internal_min_consumer());
  }

  return MaybeComputeUnknownFieldsSize(total_size, &_cached_size_);
}

const ::PROTOBUF_NAMESPACE_ID::Message::ClassData VersionDef::_class_data_ = {
    ::PROTOBUF_NAMESPACE_ID::Message::CopyWithSizeCheck,
    VersionDef::MergeImpl
};
const ::PROTOBUF_NAMESPACE_ID::Message::ClassData*VersionDef::GetClassData() const { return &_class_data_; }

void VersionDef::MergeImpl(::PROTOBUF_NAMESPACE_ID::Message* to,
                      const ::PROTOBUF_NAMESPACE_ID::Message& from) {
  static_cast<VersionDef *>(to)->MergeFrom(
      static_cast<const VersionDef &>(from));
}


void VersionDef::MergeFrom(const VersionDef& from) {
// @@protoc_insertion_point(class_specific_merge_from_start:opencv_tensorflow.VersionDef)
  GOOGLE_DCHECK_NE(&from, this);
  uint32_t cached_has_bits = 0;
  (void) cached_has_bits;

  bad_consumers_.MergeFrom(from.bad_consumers_);
  if (from._internal_producer() != 0) {
    _internal_set_producer(from._internal_producer());
  }
  if (from._internal_min_consumer() != 0) {
    _internal_set_min_consumer(from._internal_min_consumer());
  }
  _internal_metadata_.MergeFrom<::PROTOBUF_NAMESPACE_ID::UnknownFieldSet>(from._internal_metadata_);
}

void VersionDef::CopyFrom(const VersionDef& from) {
// @@protoc_insertion_point(class_specific_copy_from_start:opencv_tensorflow.VersionDef)
  if (&from == this) return;
  Clear();
  MergeFrom(from);
}

bool VersionDef::IsInitialized() const {
  return true;
}

void VersionDef::InternalSwap(VersionDef* other) {
  using std::swap;
  _internal_metadata_.InternalSwap(&other->_internal_metadata_);
  bad_consumers_.InternalSwap(&other->bad_consumers_);
  ::PROTOBUF_NAMESPACE_ID::internal::memswap<
      PROTOBUF_FIELD_OFFSET(VersionDef, min_consumer_)
      + sizeof(VersionDef::min_consumer_)
      - PROTOBUF_FIELD_OFFSET(VersionDef, producer_)>(
          reinterpret_cast<char*>(&producer_),
          reinterpret_cast<char*>(&other->producer_));
}

::PROTOBUF_NAMESPACE_ID::Metadata VersionDef::GetMetadata() const {
  return ::PROTOBUF_NAMESPACE_ID::internal::AssignDescriptors(
      &descriptor_table_versions_2eproto_getter, &descriptor_table_versions_2eproto_once,
      file_level_metadata_versions_2eproto[0]);
}

// @@protoc_insertion_point(namespace_scope)
}  // namespace opencv_tensorflow
PROTOBUF_NAMESPACE_OPEN
template<> PROTOBUF_NOINLINE ::opencv_tensorflow::VersionDef* Arena::CreateMaybeMessage< ::opencv_tensorflow::VersionDef >(Arena* arena) {
  return Arena::CreateMessageInternal< ::opencv_tensorflow::VersionDef >(arena);
}
PROTOBUF_NAMESPACE_CLOSE

// @@protoc_insertion_point(global_scope)
#include <google/protobuf/port_undef.inc>
