import { motion } from 'framer-motion'

const LoadingSpinner = () => {
  return (
    <div className="flex flex-col justify-center items-center py-20">
      <div className="relative">
        <motion.div
          className="w-24 h-24 border-2 border-amber-400/30 rounded-full"
          animate={{ scale: [1, 1.2, 1], rotate: [0, 360] }}
          transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
        />
        <motion.div
          className="w-24 h-24 border-2 border-amber-400 border-t-transparent rounded-full absolute top-0 left-0"
          animate={{ rotate: 360 }}
          transition={{ duration: 1.5, repeat: Infinity, ease: "linear" }}
        />
        <motion.div
          className="w-16 h-16 luxury-gradient rounded-full absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 glow-effect"
          animate={{ scale: [1, 1.2, 1], opacity: [0.6, 1, 0.6] }}
          transition={{ duration: 2, repeat: Infinity }}
        />
      </div>
      <motion.p 
        className="mt-6 text-amber-400 font-light text-lg elegant-text tracking-wider"
        animate={{ opacity: [0.5, 1, 0.5] }}
        transition={{ duration: 1.5, repeat: Infinity }}
      >
        Curating Collection...
      </motion.p>
    </div>
  )
}

export default LoadingSpinner

