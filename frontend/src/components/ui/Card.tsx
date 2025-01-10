export const Card: React.FC<React.PropsWithChildren<{ className?: string }>> = ({
  children,
  className = '',
}) => (
  <div className={`bg-white shadow rounded-lg p-6 ${className}`}>
    {children}
  </div>
);