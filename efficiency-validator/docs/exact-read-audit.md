# Exact-read audit protocol

The `exact-read-1` sidecar is the only filesystem evidence eligible for a
file-read efficiency verdict. The older `filesystem-trace-1` sidecar remains
useful for OS-level access diagnostics, but an `open`, path event, byte request,
or command output alone is not proof of bytes returned to the agent.

## Evidence contract

Each exact read must contain:

- the run, case, and trace identity;
- the process PID and process name;
- the canonical file path and read operation;
- the byte offset and exact byte count returned;
- the returned bytes in base64 and their SHA-256 digest;
- the SHA-256 digest of an immutable full-file snapshot.

The sidecar also records a full local snapshot for every observed regular file.
The parser verifies that the returned bytes equal the declared span of that
snapshot. For textual content it derives the touched line range from the
snapshot bytes. Binary content remains byte-exact and has no invented line
number.

The launcher appends `exact-read.trace.ended` only after the measured process
has exited and the sidecar has been flushed. A missing end record is treated as
a truncated channel and invalidates the run, even when earlier records look
complete.

## Coverage matrix

| Access mechanism | Exact mode | Rule |
| --- | --- | --- |
| `read` / `pread` | supported by the macOS interposer | returned bytes required |
| `readv` / `preadv` | supported by the macOS interposer | flattened returned bytes required |
| duplicated file descriptors | supported by the macOS interposer | descriptor lineage required |
| `mmap` with read access | unsupported by this adapter | emits a gap and invalidates the run |
| file descriptors inherited without lineage | unsupported | emits a gap and invalidates the run |
| writes or file mutation during capture | unsupported | emits a gap and invalidates the run |
| protected/two-level executable that bypasses interposition | unsupported | no exact verdict is allowed |

The privileged macOS `fs_usage` stream remains an auxiliary filesystem trace.
It can expose paths, descriptors, requested byte counts, and some offsets, but
it does not contain the bytes returned to the process. It therefore cannot
produce an `exact-read-1` verdict by itself.

All process and path categories remain in scope. The collector does not filter
out system, cache, dependency, skill, or other-repository paths to make a run
look cleaner.

## Validity

The exact trace is valid only when its metadata is available, every process
read is registered, every read has returned bytes, every file has a matching
snapshot, and every byte span is reproducible. Missing, malformed, truncated,
unsupported, or mismatched evidence makes the run invalid. The comparison
layer must not emit a file-efficiency verdict for an invalid run.

Full captured content is retained only in the explicitly authorized local
audit bundle. Reports may summarize hashes, offsets, bytes, line ranges, and
categories, but they must preserve a link to the raw evidence.

## Operational limits

- The current collector is macOS-only and relies on user-space interposition.
  Compatible flat-namespace fixtures are covered; a hardened or modern
  two-level executable that bypasses the interposer is rejected rather than
  measured approximately.
- Read-mapped files, inherited regular descriptors without lineage, file
  mutation, writes, snapshot failures, malformed records, and truncated output
  are hard gaps. They make the exact run ineligible.
- `fs_usage` can be collected with administrator authorization for broad path
  diagnostics, but its paths/byte requests are not returned content and cannot
  upgrade an exact run.
- Snapshots and returned bytes are deliberately retained in the local audit
  bundle. Treat bundles as sensitive: use restricted permissions, do not sync
  them to shared storage, and delete them according to the experiment's data
  policy.
- Snapshotting and base64 retention add overhead proportional to the files
  observed and their returned spans. Large or sensitive files should be tested
  in an explicitly authorized audit mode; reducing retention would change the
  evidence contract and therefore invalidate the run.
- Process-tree sampling is a coverage check, not a replacement for process
  instrumentation. Any PID in the measured tree that is absent from the exact
  sidecar invalidates the run.
