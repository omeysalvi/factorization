import pyopencl as cl
import numpy as np

semiprime = 99872105682048729193
chunks = []
temp = semiprime
for _ in range(5):
    chunks.append(temp & 0xFFFF)
    temp >>= 16

ctx = cl.create_some_context(interactive=False)
queue = cl.CommandQueue(ctx)

prg = cl.Program(ctx, """
__kernel void test_mod(
    const ulong chunk4,
    const ulong chunk3,
    const ulong chunk2,
    const ulong chunk1,
    const ulong chunk0,
    __global const ulong *candidates,
    __global ulong *results
) {
    int gid = get_global_id(0);
    ulong candidate = candidates[gid];
    
    ulong rem = 0;
    rem = ((rem << 16) + chunk4) % candidate;
    rem = ((rem << 16) + chunk3) % candidate;
    rem = ((rem << 16) + chunk2) % candidate;
    rem = ((rem << 16) + chunk1) % candidate;
    rem = ((rem << 16) + chunk0) % candidate;
    
    results[gid] = rem;
}
""").build()

candidates = np.array([9999925913, 9987284561, 123456], dtype=np.uint64)
mf = cl.mem_flags
candidates_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=candidates)
results_buf = cl.Buffer(ctx, mf.WRITE_ONLY, candidates.nbytes)
results = np.empty_like(candidates)

prg.test_mod(queue, candidates.shape, None, 
             np.uint64(chunks[4]), np.uint64(chunks[3]), np.uint64(chunks[2]), 
             np.uint64(chunks[1]), np.uint64(chunks[0]), 
             candidates_buf, results_buf)

cl.enqueue_copy(queue, results, results_buf)
print("Results:", results)
