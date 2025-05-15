import math

def pipe_diameter_for_velocity(flow_lps, max_velocity=3.0):
    """
    Calculate the minimum internal diameter (in mm) of a pipe required 
    to keep the velocity below the specified max_velocity (default 3 m/s),
    given the flow rate in L/s.

    Parameters:
    - flow_lps: Flow rate in litres per second (L/s)
    - max_velocity: Maximum allowable velocity in m/s (default = 3.0)

    Returns:
    - Minimum internal diameter in mm
    """
    Q = flow_lps / 1000  # Convert to m³/s
    A = Q / max_velocity  # Required area in m²
    D = math.sqrt(4 * A / math.pi)  # Diameter in meters
    
    print(f"Required internal diameter to keep velocity ≤ 3 m/s: {D*1000} mm")

    return round(D * 1000, 1)  # Return diameter in mm


if __name__ == "__main__":
    # Example usage
    flow = 757  # L/s
    required_diameter = pipe_diameter_for_velocity(flow)
    print(f"Required internal diameter to keep velocity ≤ 3 m/s: {required_diameter} mm")
