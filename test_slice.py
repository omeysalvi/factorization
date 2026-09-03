import pyopencl as cl
import numpy as np
import math

prime1 = 9999925913
prime2 = 9987284561
semiprime = prime1 * prime2

sample_range = 1000000
theta_step = (math.pi / 2) / sample_range

# Just slice around the known good index
start_idx = 499500
end_idx = 499700

base_nums = []
for i in range(start_idx, end_idx):
    theta = i * theta_step
    r_value = int(math.sqrt(2 * semiprime / math.sin(2 * theta)))
    base_nums.append(int(r_value * math.cos(theta)))

base_nums = np.array(base_nums, dtype=np.uint64)

chunks = []
temp = semiprime
for _ in range(5):
    chunks.append(temp & 0xFFFF)
    temp >>= 16

ctx = cl.create_some_context(interactive=False)
queue = cl.CommandQueue(ctx)

kernel_code = """
__kernel void find_factors(
    __global const ulong *base_nums,
    const ulong chunk4,
    const ulong chunk3,
    const ulong chunk2,
    const ulong chunk1,
    const ulong chunk0,
    const int walk_samples,
    __global ulong *found_factor
) {
    int gid = get_global_id(0);
    ulong base_num = base_nums[gid];
    
    if (*found_factor != 0) return;

    int steps = 0;
    int iters = 0;
    int max_iters = walk_samples * 10;
    ulong num = base_num;
    while (steps < walk_samples && iters < max_iters) {
        iters++;
        if (num > 1 && num % 2 != 0 && num % 3 != 0) {
            ulong rem = 0;
            rem = ((rem << 16) + chunk4) % num;
            rem = ((rem << 16) + chunk3) % num;
            rem = ((rem << 16) + chunk2) % num;
            rem = ((rem << 16) + chunk1) % num;
            rem = ((rem << 16) + chunk0) % num;
            
            if (rem == 0) {
                *found_factor = num;
                return;
            }
            steps++;
        }
        num++;
    }
    
    steps = 0;
    iters = 0;
    num = base_num;
    while (steps < walk_samples && iters < max_iters) {
        iters++;
        if (num == 0) break;
        if (num > 1 && num % 2 != 0 && num % 3 != 0) {
            ulong rem = 0;
            rem = ((rem << 16) + chunk4) % num;
            rem = ((rem << 16) + chunk3) % num;
            rem = ((rem << 16) + chunk2) % num;
            rem = ((rem << 16) + chunk1) % num;
            rem = ((rem << 16) + chunk0) % num;
            
            if (rem == 0) {
                *found_factor = num;
                return;
            }
            steps++;
        }
        num--;
    }
}
"""

prg = cl.Program(ctx, kernel_code).build()
mf = cl.mem_flags
base_nums_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=base_nums)
found_factor_arr = np.zeros(1, dtype=np.uint64)
found_factor_buf = cl.Buffer(ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=found_factor_arr)

prg.find_factors(queue, base_nums.shape, None,
                 base_nums_buf,
                 np.uint64(chunks[4]), np.uint64(chunks[3]),
                 np.uint64(chunks[2]), np.uint64(chunks[1]), np.uint64(chunks[0]),
                 np.int32(5000),
                 found_factor_buf)

cl.enqueue_copy(queue, found_factor_arr, found_factor_buf).wait()
print('Found factor slice:', found_factor_arr[0])
