/** Like window.setTimeout, but returns a promise of the result of the function once it runs */
function promiseTimeout<T>(f: () => T, timeout: number): Promise<T> {
    return new Promise((resolve, reject) => {
        setTimeout(async () => {
            try {
                resolve(f())
            } catch(e) {
                reject(e);
            }
        }, timeout);
    })
}

/**
 * Ensures that a function is only run when no further calls occur within the next delay milliseconds. 
 * @param f Function to run
 * @param delay Number of milliseconds to wait until the function should be run
 */
export default function debounce<T>(f: () => Promise<T>, delay: number): () => Promise<T | null> {
    let global_call_id = 0;

    return async function() {
        // increase the global count id, and store the current one
        global_call_id++;
        const this_call_id = global_call_id;

        return promiseTimeout(() => {
            // if something else called in the meantime, return
            if(this_call_id !== global_call_id) return null;

            // else run this function
            return f();
        }, delay);
    }
}