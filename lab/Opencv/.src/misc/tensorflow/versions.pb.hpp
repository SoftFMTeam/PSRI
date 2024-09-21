// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: versions.proto

#ifndef GOOGLE_PROTOBUF_INCLUDED_versions_2eproto
#define GOOGLE_PROTOBUF_INCLUDED_versions_2eproto

#include <limits>
#include <string>

#include <google/protobuf/port_def.inc>
#if PROTOBUF_VERSION < 3019000
#error This file was generated by a newer version of protoc which is
#error incompatible with your Protocol Buffer headers. Please update
#error your headers.
#endif
#if 3019001 < PROTOBUF_MIN_PROTOC_VERSION
#error This file was generated by an older version of protoc which is
#error incompatible with your Protocol Buffer headers. Please
#error regenerate this file with a newer version of protoc.
#endif

#include <google/protobuf/port_undef.inc>
#include <google/protobuf/io/coded_stream.hpp>
#include <google/protobuf/arena.hpp>
#include <google/protobuf/arenastring.hpp>
#include <google/protobuf/generated_message_table_driven.hpp>
#include <google/protobuf/generated_message_util.hpp>
#include <google/protobuf/metadata_lite.hpp>
#include <google/protobuf/generated_message_reflection.hpp>
#include <google/protobuf/message.hpp>
#include <google/protobuf/repeated_field.hpp>  // IWYU pragma: export
#include <google/protobuf/extension_set.hpp>  // IWYU pragma: export
#include <google/protobuf/unknown_field_set.hpp>
// @@protoc_insertion_point(includes)
#include <google/protobuf/port_def.inc>
#define PROTOBUF_INTERNAL_EXPORT_versions_2eproto
PROTOBUF_NAMESPACE_OPEN
namespace internal {
class AnyMetadata;
}  // namespace internal
PROTOBUF_NAMESPACE_CLOSE

// Internal implementation detail -- do not use these members.
struct TableStruct_versions_2eproto {
  static const ::PROTOBUF_NAMESPACE_ID::internal::ParseTableField entries[]
    PROTOBUF_SECTION_VARIABLE(protodesc_cold);
  static const ::PROTOBUF_NAMESPACE_ID::internal::AuxiliaryParseTableField aux[]
    PROTOBUF_SECTION_VARIABLE(protodesc_cold);
  static const ::PROTOBUF_NAMESPACE_ID::internal::ParseTable schema[1]
    PROTOBUF_SECTION_VARIABLE(protodesc_cold);
  static const ::PROTOBUF_NAMESPACE_ID::internal::FieldMetadata field_metadata[];
  static const ::PROTOBUF_NAMESPACE_ID::internal::SerializationTable serialization_table[];
  static const uint32_t offsets[];
};
extern const ::PROTOBUF_NAMESPACE_ID::internal::DescriptorTable descriptor_table_versions_2eproto;
namespace opencv_tensorflow {
class VersionDef;
struct VersionDefDefaultTypeInternal;
extern VersionDefDefaultTypeInternal _VersionDef_default_instance_;
}  // namespace opencv_tensorflow
PROTOBUF_NAMESPACE_OPEN
template<> ::opencv_tensorflow::VersionDef* Arena::CreateMaybeMessage<::opencv_tensorflow::VersionDef>(Arena*);
PROTOBUF_NAMESPACE_CLOSE
namespace opencv_tensorflow {

// ===================================================================

class VersionDef final :
    public ::PROTOBUF_NAMESPACE_ID::Message /* @@protoc_insertion_point(class_definition:opencv_tensorflow.VersionDef) */ {
 public:
  inline VersionDef() : VersionDef(nullptr) {}
  ~VersionDef() override;
  explicit constexpr VersionDef(::PROTOBUF_NAMESPACE_ID::internal::ConstantInitialized);

  VersionDef(const VersionDef& from);
  VersionDef(VersionDef&& from) noexcept
    : VersionDef() {
    *this = ::std::move(from);
  }

  inline VersionDef& operator=(const VersionDef& from) {
    CopyFrom(from);
    return *this;
  }
  inline VersionDef& operator=(VersionDef&& from) noexcept {
    if (this == &from) return *this;
    if (GetOwningArena() == from.GetOwningArena()
  #ifdef PROTOBUF_FORCE_COPY_IN_MOVE
        && GetOwningArena() != nullptr
  #endif  // !PROTOBUF_FORCE_COPY_IN_MOVE
    ) {
      InternalSwap(&from);
    } else {
      CopyFrom(from);
    }
    return *this;
  }

  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* descriptor() {
    return GetDescriptor();
  }
  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* GetDescriptor() {
    return default_instance().GetMetadata().descriptor;
  }
  static const ::PROTOBUF_NAMESPACE_ID::Reflection* GetReflection() {
    return default_instance().GetMetadata().reflection;
  }
  static const VersionDef& default_instance() {
    return *internal_default_instance();
  }
  static inline const VersionDef* internal_default_instance() {
    return reinterpret_cast<const VersionDef*>(
               &_VersionDef_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    0;

  friend void swap(VersionDef& a, VersionDef& b) {
    a.Swap(&b);
  }
  inline void Swap(VersionDef* other) {
    if (other == this) return;
  #ifdef PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() != nullptr &&
        GetOwningArena() == other->GetOwningArena()) {
   #else  // PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() == other->GetOwningArena()) {
  #endif  // !PROTOBUF_FORCE_COPY_IN_SWAP
      InternalSwap(other);
    } else {
      ::PROTOBUF_NAMESPACE_ID::internal::GenericSwap(this, other);
    }
  }
  void UnsafeArenaSwap(VersionDef* other) {
    if (other == this) return;
    GOOGLE_DCHECK(GetOwningArena() == other->GetOwningArena());
    InternalSwap(other);
  }

  // implements Message ----------------------------------------------

  VersionDef* New(::PROTOBUF_NAMESPACE_ID::Arena* arena = nullptr) const final {
    return CreateMaybeMessage<VersionDef>(arena);
  }
  using ::PROTOBUF_NAMESPACE_ID::Message::CopyFrom;
  void CopyFrom(const VersionDef& from);
  using ::PROTOBUF_NAMESPACE_ID::Message::MergeFrom;
  void MergeFrom(const VersionDef& from);
  private:
  static void MergeImpl(::PROTOBUF_NAMESPACE_ID::Message* to, const ::PROTOBUF_NAMESPACE_ID::Message& from);
  public:
  PROTOBUF_ATTRIBUTE_REINITIALIZES void Clear() final;
  bool IsInitialized() const final;

  size_t ByteSizeLong() const final;
  const char* _InternalParse(const char* ptr, ::PROTOBUF_NAMESPACE_ID::internal::ParseContext* ctx) final;
  uint8_t* _InternalSerialize(
      uint8_t* target, ::PROTOBUF_NAMESPACE_ID::io::EpsCopyOutputStream* stream) const final;
  int GetCachedSize() const final { return _cached_size_.Get(); }

  private:
  void SharedCtor();
  void SharedDtor();
  void SetCachedSize(int size) const final;
  void InternalSwap(VersionDef* other);

  private:
  friend class ::PROTOBUF_NAMESPACE_ID::internal::AnyMetadata;
  static ::PROTOBUF_NAMESPACE_ID::StringPiece FullMessageName() {
    return "opencv_tensorflow.VersionDef";
  }
  protected:
  explicit VersionDef(::PROTOBUF_NAMESPACE_ID::Arena* arena,
                       bool is_message_owned = false);
  private:
  static void ArenaDtor(void* object);
  inline void RegisterArenaDtor(::PROTOBUF_NAMESPACE_ID::Arena* arena);
  public:

  static const ClassData _class_data_;
  const ::PROTOBUF_NAMESPACE_ID::Message::ClassData*GetClassData() const final;

  ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadata() const final;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  enum : int {
    kBadConsumersFieldNumber = 3,
    kProducerFieldNumber = 1,
    kMinConsumerFieldNumber = 2,
  };
  // repeated int32 bad_consumers = 3;
  int bad_consumers_size() const;
  private:
  int _internal_bad_consumers_size() const;
  public:
  void clear_bad_consumers();
  private:
  int32_t _internal_bad_consumers(int index) const;
  const ::PROTOBUF_NAMESPACE_ID::RepeatedField< int32_t >&
      _internal_bad_consumers() const;
  void _internal_add_bad_consumers(int32_t value);
  ::PROTOBUF_NAMESPACE_ID::RepeatedField< int32_t >*
      _internal_mutable_bad_consumers();
  public:
  int32_t bad_consumers(int index) const;
  void set_bad_consumers(int index, int32_t value);
  void add_bad_consumers(int32_t value);
  const ::PROTOBUF_NAMESPACE_ID::RepeatedField< int32_t >&
      bad_consumers() const;
  ::PROTOBUF_NAMESPACE_ID::RepeatedField< int32_t >*
      mutable_bad_consumers();

  // int32 producer = 1;
  void clear_producer();
  int32_t producer() const;
  void set_producer(int32_t value);
  private:
  int32_t _internal_producer() const;
  void _internal_set_producer(int32_t value);
  public:

  // int32 min_consumer = 2;
  void clear_min_consumer();
  int32_t min_consumer() const;
  void set_min_consumer(int32_t value);
  private:
  int32_t _internal_min_consumer() const;
  void _internal_set_min_consumer(int32_t value);
  public:

  // @@protoc_insertion_point(class_scope:opencv_tensorflow.VersionDef)
 private:
  class _Internal;

  template <typename T> friend class ::PROTOBUF_NAMESPACE_ID::Arena::InternalHelper;
  typedef void InternalArenaConstructable_;
  typedef void DestructorSkippable_;
  ::PROTOBUF_NAMESPACE_ID::RepeatedField< int32_t > bad_consumers_;
  mutable std::atomic<int> _bad_consumers_cached_byte_size_;
  int32_t producer_;
  int32_t min_consumer_;
  mutable ::PROTOBUF_NAMESPACE_ID::internal::CachedSize _cached_size_;
  friend struct ::TableStruct_versions_2eproto;
};
// ===================================================================


// ===================================================================

#ifdef __GNUC__
  #pragma GCC diagnostic push
  #pragma GCC diagnostic ignored "-Wstrict-aliasing"
#endif  // __GNUC__
// VersionDef

// int32 producer = 1;
inline void VersionDef::clear_producer() {
  producer_ = 0;
}
inline int32_t VersionDef::_internal_producer() const {
  return producer_;
}
inline int32_t VersionDef::producer() const {
  // @@protoc_insertion_point(field_get:opencv_tensorflow.VersionDef.producer)
  return _internal_producer();
}
inline void VersionDef::_internal_set_producer(int32_t value) {

  producer_ = value;
}
inline void VersionDef::set_producer(int32_t value) {
  _internal_set_producer(value);
  // @@protoc_insertion_point(field_set:opencv_tensorflow.VersionDef.producer)
}

// int32 min_consumer = 2;
inline void VersionDef::clear_min_consumer() {
  min_consumer_ = 0;
}
inline int32_t VersionDef::_internal_min_consumer() const {
  return min_consumer_;
}
inline int32_t VersionDef::min_consumer() const {
  // @@protoc_insertion_point(field_get:opencv_tensorflow.VersionDef.min_consumer)
  return _internal_min_consumer();
}
inline void VersionDef::_internal_set_min_consumer(int32_t value) {

  min_consumer_ = value;
}
inline void VersionDef::set_min_consumer(int32_t value) {
  _internal_set_min_consumer(value);
  // @@protoc_insertion_point(field_set:opencv_tensorflow.VersionDef.min_consumer)
}

// repeated int32 bad_consumers = 3;
inline int VersionDef::_internal_bad_consumers_size() const {
  return bad_consumers_.size();
}
inline int VersionDef::bad_consumers_size() const {
  return _internal_bad_consumers_size();
}
inline void VersionDef::clear_bad_consumers() {
  bad_consumers_.Clear();
}
inline int32_t VersionDef::_internal_bad_consumers(int index) const {
  return bad_consumers_.Get(index);
}
inline int32_t VersionDef::bad_consumers(int index) const {
  // @@protoc_insertion_point(field_get:opencv_tensorflow.VersionDef.bad_consumers)
  return _internal_bad_consumers(index);
}
inline void VersionDef::set_bad_consumers(int index, int32_t value) {
  bad_consumers_.Set(index, value);
  // @@protoc_insertion_point(field_set:opencv_tensorflow.VersionDef.bad_consumers)
}
inline void VersionDef::_internal_add_bad_consumers(int32_t value) {
  bad_consumers_.Add(value);
}
inline void VersionDef::add_bad_consumers(int32_t value) {
  _internal_add_bad_consumers(value);
  // @@protoc_insertion_point(field_add:opencv_tensorflow.VersionDef.bad_consumers)
}
inline const ::PROTOBUF_NAMESPACE_ID::RepeatedField< int32_t >&
VersionDef::_internal_bad_consumers() const {
  return bad_consumers_;
}
inline const ::PROTOBUF_NAMESPACE_ID::RepeatedField< int32_t >&
VersionDef::bad_consumers() const {
  // @@protoc_insertion_point(field_list:opencv_tensorflow.VersionDef.bad_consumers)
  return _internal_bad_consumers();
}
inline ::PROTOBUF_NAMESPACE_ID::RepeatedField< int32_t >*
VersionDef::_internal_mutable_bad_consumers() {
  return &bad_consumers_;
}
inline ::PROTOBUF_NAMESPACE_ID::RepeatedField< int32_t >*
VersionDef::mutable_bad_consumers() {
  // @@protoc_insertion_point(field_mutable_list:opencv_tensorflow.VersionDef.bad_consumers)
  return _internal_mutable_bad_consumers();
}

#ifdef __GNUC__
  #pragma GCC diagnostic pop
#endif  // __GNUC__

// @@protoc_insertion_point(namespace_scope)

}  // namespace opencv_tensorflow

// @@protoc_insertion_point(global_scope)

#include <google/protobuf/port_undef.inc>
#endif  // GOOGLE_PROTOBUF_INCLUDED_GOOGLE_PROTOBUF_INCLUDED_versions_2eproto
